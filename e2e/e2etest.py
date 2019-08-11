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

import subprocess
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

    def guet_init(self) -> subprocess.Popen:
        process = subprocess.Popen(['guet', 'init'])
        process.wait()
        return process

    def guet_add(self, initials: str, name: str, email: str) -> subprocess.Popen:
        process = subprocess.Popen(['guet', 'add', initials, name, email])
        process.wait()
        return process

    def guet_set(self, initials: [str], directory_to_execute_in: str = None) -> subprocess.Popen:
        if directory_to_execute_in is None:
            process = subprocess.Popen(['guet', 'set'] + initials)
            process.wait()
            return process
        else:
            process = subprocess.Popen(['guet', 'set'] + initials, cwd=directory_to_execute_in)
            process.wait()
            return process

    def guet_start(self, use_python3: bool = True, directory_to_execute_in: str = None):
        args = ['guet', 'start']
        if use_python3:
            args.append('--python3')
        if directory_to_execute_in is None:
            process = subprocess.Popen(args)
            process.wait()
        else:
            process = subprocess.Popen(args, cwd=directory_to_execute_in)
            process.wait()

    def git_commit(self, message: str, directory_to_execute_in: str) -> subprocess.Popen:
        process = subprocess.Popen(['git', 'commit', '-m', message], cwd=directory_to_execute_in)
        process.wait()
        return process

    def git_add(self, files_to_add: str, directory_to_execute_in: str) -> subprocess.Popen:
        process = subprocess.Popen(['git', 'add', files_to_add], cwd=directory_to_execute_in)
        process.wait()
        return process

    def git_init(self, path_to_init: str, directory_to_execute_in: str) -> subprocess.Popen:
        process = subprocess.Popen(['git', 'init', path_to_init], cwd=directory_to_execute_in)
        process.wait()
        return process

    def git_log(self, directory_to_execute: str) -> str:
        process = subprocess.Popen(['git', 'log'], stdout=subprocess.PIPE, cwd=directory_to_execute)
        return process.communicate()[0].decode('utf-8')
