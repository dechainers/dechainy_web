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
import threading
import unittest
import requests
import os
import time

from dechainy_web import bp
from dechainy.controller import Controller


from flask import Flask

base_url = "http://localhost:5000"

controller = Controller()
app = None
t = None


@unittest.skipIf(os.getuid(), reason='Root for BCC')
class TestPlugin(unittest.TestCase):

    @staticmethod
    def my_thread():
        app = Flask(TestPlugin.__name__)
        app.register_blueprint(bp)
        app.run()

    @classmethod
    def setUpClass(cls) -> None:
        t = threading.Thread(target=TestPlugin.my_thread, daemon=True)
        t.start()
        time.sleep(5)

    def test1_health_check(self):
        res = requests.get(base_url)
        res.raise_for_status()


if __name__ == '__main__':
    unittest.main()
