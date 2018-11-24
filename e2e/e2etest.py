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

import unittest
from os import mkdir, chdir, getcwd
from os.path import abspath, join, expanduser, isdir
from shutil import rmtree

from guet import constants as const


class E2ETest(unittest.TestCase):

    def _test_dir(self):
        return 'test-env'

    def setUp(self):
        path = join(expanduser('~'), self._test_dir())
        if isdir(path):
            rmtree(path)
        mkdir(path)
        self.testcwd = abspath(path)
        self.current_cwd = getcwd()
        chdir(self.testcwd)
        self.before()

    def tearDown(self):
        chdir(self.current_cwd)
        rmtree(join(expanduser('~'), self._test_dir()))
        self.after()

    def after(self):
        app_path = join(expanduser('~'), const.APP_FOLDER_NAME)
        if isdir(app_path):
            rmtree(join(expanduser('~'), '.guet'))

    def before(self):
        pass

    def _parse_output(self, process):
        output = ''
        for line in process.stdout.readlines():
            output += line.decode('utf-8')
        return output
