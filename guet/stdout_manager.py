"""
Copyright 2018 Christopher M. Boyer

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

    http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.
"""


class StdoutManager:

    _instance = None

    def __init__(self):
        if self._instance is None:
            StdoutManager._instance = self
        import sys
        self._stdout = sys.__stdout__

    @classmethod
    def get_instance(cls):
        if not cls._instance:
            cls._instance = StdoutManager()
        return cls._instance

    def get_stdout(self):
        return self._stdout

    def set_stdout(self, stdout):
        self._stdout = stdout
