# Copyright 2022 DeChainers
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#    http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
import os
import importlib
import zipfile

from types import ModuleType
from typing import List, Union
from flask import request, abort, Blueprint, current_app, jsonify

from dechainy import exceptions
from dechainy.plugins import Probe

project_url = "https://github.com/dechainers/dechainy_web"
version = "1.0"

bp = Blueprint('main', __name__)


@bp.route('/probes', methods=['GET', 'DELETE'])
@bp.route('/probes/<plugin_name>', methods=['GET', 'POST', 'DELETE'])
@bp.route('/probes/<plugin_name>/<probe_name>', methods=['GET', 'DELETE'])
def manage_probe(plugin_name: str = None, probe_name: str = None) -> Probe:
    """Rest endpoint to get, create or modify an instance of a given Plugin

    Args:
        plugin_name (str): The name of the Plugin
        probe_name (str): The name of the instance

    Returns:
        Union[ProbeConfig, str]: The instance if GET, else its name
    """
    try:
        if request.method == 'DELETE':
            current_app.config['controller'].delete_probe(
                plugin_name, probe_name)
            return ""
        if request.method == 'POST':
            if not request.json:
                abort(400, 'A configuration is needed')

            probe = getattr(current_app.config['controller'].get_plugin(
                plugin_name), plugin_name.capitalize())(**request.json)
            current_app.config['controller'].create_probe(probe)
            return "", 201
        return jsonify(current_app.config['controller'].get_probe(plugin_name, probe_name))
    except (exceptions.PluginNotFoundException,
            exceptions.ProbeNotFoundException,
            exceptions.ProbeAlreadyExistsException) as e:
        abort(404, e)


@bp.route(f'/probes/<plugin_name>/<probe_name>/<program_type>/metrics', methods=['GET'])
@bp.route(f'/probes/<plugin_name>/<probe_name>/<program_type>/metrics/<metric_name>', methods=['GET'])
def retrieve_metric(plugin_name: str, probe_name: str, program_type: str, metric_name: str = None) -> any:
    """Rest endpoint to retrieve the value of a defined metric

    Args:
        plugin_name (str): The name of the plugin
        probe_name (str): The name of the Adaptmon instance
        program_type (str): The type of the program (Ingress/Egress)
        metric_name (str): The name of the metric to be retrieved

    Returns:
        any: The value of the metric
    """
    try:
        return jsonify(current_app.config['controller'].get_probe(plugin_name, probe_name)
                       .retrieve_metric(program_type, metric_name))
    except (exceptions.ProbeNotFoundException, LookupError) as e:
        abort(404, e)


@bp.route('/plugins', methods=['GET', 'POST', 'PUT', 'DELETE'])
@bp.route('/plugins/<plugin_name>', methods=['DELETE'])
def manage_plugin(plugin_name: str = None) -> Union[ModuleType, List[ModuleType]]:
    """Rest endpoint to get, create or modify an instance of a given Plugin

    Args:
        plugin_name (str): The name of the Plugin
        probe_name (str): The name of the instance

    Returns:
        Union[ProbeConfig, str]: The instance if GET, else its name
    """
    try:
        if request.method == 'DELETE':
            current_app.config['controller'].delete_plugin(plugin_name)
            return ""
        elif request.method in ['POST', 'PUT']:
            if request.files["zip"]:
                target = os.path.join(
                    os.sep, "tmp", request.files["zip"].filename.split(".")[0])
                with zipfile.ZipFile(request.files["zip"].stream._file, 'r') as zip:
                    zip.extractall(os.path.join(os.sep, "tmp"))
                current_app.config['controller'].create_plugin(
                    target, update=request.method == 'PUT')
            elif request.form["name"]:
                target = os.path.join(os.sep, "tmp", request.form["name"])
                current_app.config['controller'].create_plugin(
                    request.form["name"], update=request.method == 'PUT')
            else:
                abort(400, 'A name for the plugin is needed')

            plugin_name = os.path.basename(target)
            plugin_module = 'dechainy.plugins.{}.routes'.format(plugin_name)
            if importlib.util.find_spec(plugin_module):
                module = importlib.import_module(plugin_module)
                if not hasattr(module, "bp"):
                    current_app.config['controller'].delete_plugin(plugin_name)
                    raise exceptions.InvalidPluginException(
                        "Routes for Plugin {} are invalid".format(plugin_name))
                current_app.register_blueprint(module.bp)

            return "", 201 if request.method == "POST" else 200

        return jsonify(current_app.config['controller'].get_plugin())
    except exceptions.PluginNotFoundException as e:
        abort(404, e)
    except (exceptions.PluginAlreadyExistsException, exceptions.InvalidPluginException) as e:
        abort(400, e)


@bp.route('/')
def __index() -> str:
    """Rest endpoint to test whether the server is correctly working

    Returns:
        str: The default message string
    """
    return 'DeChainy server greets you :D'
