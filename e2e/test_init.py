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
from os.path import join, expanduser, isfile
from e2e.e2etest import E2ETest
from guet import constants as const
from guet.commands.init import InitDataSourceCommand


class TestInit(E2ETest):

    def _test_dir(self):
        return 'test-env'

    def test_successful_init(self):
        process = subprocess.Popen(['guet', 'init'])
        process.wait()
        self.assertTrue(join(expanduser('~'), '.guet'))

    def test_multiple_calls_to_init_tells_user_config_folder_already_exists(self):
        process = subprocess.Popen(['guet', 'init'])
        process.wait()
        process = subprocess.Popen(['guet', 'init'], stdout=subprocess.PIPE)
        process.wait()
        self.assertEqual('Config folder already exists.\n', self._parse_output(process))
        process.stdout.close()

    def test_init_creates_guet_authors_file(self):
        process = subprocess.Popen(['guet', 'init'])
        process.wait()
        path = join(expanduser('~'), const.APP_FOLDER_NAME, const.COMMITTER_NAMES)
        file_exists = isfile(path)
        self.assertTrue(file_exists)

    def test_init_prints_help_message_when_given_invalid_arguments(self):
        process = subprocess.Popen(['guet', 'init', 'extra'], stdout=subprocess.PIPE)
        process.wait()
        expected = 'Invalid arguments.\n\n   {}\n'.format(InitDataSourceCommand([]).help())
        actual = self._parse_output(process)
        self.assertEqual(expected, actual)
        process.stdout.close()
