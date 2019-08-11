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
from os.path import join, isfile

from e2e.e2etest import E2ETest


class TestStart(E2ETest):

    def _test_dir(self):
        return 'test-env'

    def test_start_guet_creates_hook_git_folder_in_current_path(self):
        process = subprocess.Popen(['git', 'init'], stdout=subprocess.PIPE)
        process.wait()
        process.stdout.close()
        process = subprocess.Popen(['guet', 'start'])
        process.wait()
        self.assertTrue(join(self.testcwd, '.git', 'hooks', 'commit-msg'))

    def test_start_tells_user_that_a_git_folder_does_not_exist(self):
        process = subprocess.Popen(['guet', 'start'], stdout=subprocess.PIPE)
        process.wait()
        output = self._parse_output(process)
        process.stdout.close()
        self.assertEqual('Git not initialized in this directory.\n', output)

    def test_start_tells_user_when_there_is_already_a_pre_commit_hook_and_gives_options_and_can_choose_to_cancel(self):
        process = subprocess.Popen(['git', 'init'])
        process.wait()
        f = open(join(self.testcwd, '.git', 'hooks', 'pre-commit'), 'w+')
        f.close()
        process = subprocess.Popen(['guet', 'start'], stderr=subprocess.PIPE, stdout=subprocess.PIPE, stdin=subprocess.PIPE)
        output = process.communicate('x'.encode())
        process.wait()
        self.assertEqual('There is already commit hooks in this project. Would you like to overwrite (o), create (c) the file and put it in the hooks folder, or cancel (x)?\n', output[0].decode('utf-8'))

    def test_start_tells_user_when_there_is_already_a_pre_commit_hook_and_gives_options_and_can_choose_to_overwrite(self):
        process = subprocess.Popen(['git', 'init'])
        process.wait()
        f = open(join(self.testcwd, '.git', 'hooks', 'pre-commit'), 'w+')
        f.write('Text')
        f.close()
        process = subprocess.Popen(['guet', 'start'], stderr=subprocess.PIPE, stdout=subprocess.PIPE, stdin=subprocess.PIPE)
        output = process.communicate('o'.encode())
        process.wait()
        self.assertEqual('There is already commit hooks in this project. Would you like to overwrite (o), create (c) the file and put it in the hooks folder, or cancel (x)?\n', output[0].decode('utf-8'))

        f = open(join(self.testcwd, '.git', 'hooks', 'pre-commit'), 'r')
        data = f.readlines()
        f.close()
        self.assertNotEqual(1, len(data), 'Should have more than one line because pre-commit file is being overwritten')

    def test_creates_pre_commit_and_post_commit_with_python_shebang_by_default(self):
        process = subprocess.Popen(['git', 'init'], stdout=subprocess.PIPE)
        process.wait()
        process.stdout.close()
        process = subprocess.Popen(['guet', 'start'])
        process.wait()
        self._file_should_have_shell_as_shebang('pre-commit', 'python')
        self._file_should_have_shell_as_shebang('post-commit', 'python')

    def test_start_can_be_given_python3_flag_to_chhange_shebang_to_python3(self):
        process = subprocess.Popen(['git', 'init'], stdout=subprocess.PIPE)
        process.wait()
        process.stdout.close()
        process = subprocess.Popen(['guet', 'start', '--python3'])
        process.wait()
        self._file_should_have_shell_as_shebang('pre-commit', 'python3')
        self._file_should_have_shell_as_shebang('post-commit', 'python3')

    def _file_should_have_shell_as_shebang(self, file_name: str, interpreter: str):
        with open(join(self.testcwd, '.git', 'hooks', file_name)) as f:
            first_line = f.readline().rstrip()
        self.assertTrue(first_line.endswith(interpreter), '{} should end in {}'.format(first_line, 'python'))
