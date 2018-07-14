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

from e2e.e2etest import E2ETest
import subprocess
from os.path import join


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
