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
import argparse
import logging
from importlib import import_module
from importlib.util import find_spec

from dechainy.controller import Controller
from flask import Flask

from . import bp


def _parse_arguments():
    """Method to define and parse command line arguments.

    Returns:
        Dict[str, any]: The dictionary of arguments.
    """
    parser = argparse.ArgumentParser(
        formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    parser.add_argument('-a', '--address',
                        help='server address', type=str, default='0.0.0.0')
    parser.add_argument('-p', '--port', help='server port',
                        type=int, default=5000)
    parser.add_argument('-l', '--log-level', help='dechainy log level',
                        type=str, default="INFO")
    parser.add_argument(
        '-d', '--debug', help='server debug mode', action="store_true")
    return parser.parse_args().__dict__


def main():
    """Method to run the main module, provided the defined arguments.
    By default, a web server is created and all the routes belonging to
    the available plugins are loaded.
    """
    args = _parse_arguments()
    ctr = Controller(log_level=logging._nameToLevel[args["log_level"]])
    app = Flask(__name__)
    app.register_blueprint(bp)
    for plugin in ctr.get_plugin():
        target = 'dechainy.plugins.{}.routes'.format(plugin)
        # dynamically load per-plugin routes if any
        if find_spec(target):
            module = import_module(target)
            app.register_blueprint(module.bp)
    app.run(host=args["address"], port=args["port"],
            debug=args["debug"], use_reloader=False)


if __name__ == '__main__':
    main()
