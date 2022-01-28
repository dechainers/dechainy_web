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
from flask import Flask

from dechainy.controller import Controller
from . import bp


def _parse_arguments():
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
    """Function used when the module is called as main file. It provides, given the provided (or not)
    startup file, a running Controller and optionally a REST server
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
    app.config['controller'] = ctr
    app.run(host=args["address"], port=args["port"],
            debug=args["debug"], use_reloader=False)


if __name__ == '__main__':
    main()
