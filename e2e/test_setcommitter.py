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
from os.path import join, expanduser
from guet import constants as const
import subprocess


class TestGuetSet(E2ETest):

    def test_set_adds_given_users_to_committers_file(self):
        process = subprocess.Popen(['guet', 'init'])
        process.wait()
        initials = 'initials'
        name = 'name'
        email = 'user@localhost'
        process = subprocess.Popen(['guet', 'add', initials, name, email])
        process.wait()
        process = subprocess.Popen(['guet', 'set', initials])
        process.wait()

        data_source_path = join(expanduser('~'), const.APP_FOLDER_NAME, const.COMMITTER_NAMES)

        with open(data_source_path) as committer_names:
            content = committer_names.readlines()

        self.assertEqual('{} <{}>\n'.format(name, email), content[0])

    def test_set_adds_multiple_users_to_committers_file(self):
        process = subprocess.Popen(['guet', 'init'])
        process.wait()
        initials = 'initials'
        initials2 = 'initials2'
        name = 'name'
        email = 'user@localhost'
        process = subprocess.Popen(['guet', 'add', initials, name, email])
        process.wait()
        process = subprocess.Popen(['guet', 'add', initials2, name, email])
        process.wait()
        process = subprocess.Popen(['guet', 'set', initials, initials2])
        process.wait()

        data_source_path = join(expanduser('~'), const.APP_FOLDER_NAME, const.COMMITTER_NAMES)

        with open(data_source_path) as committer_names:
            content = committer_names.readlines()

        self.assertEqual('{} <{}>\n'.format(name, email), content[0])
        self.assertEqual('{} <{}>\n'.format(name, email), content[1])