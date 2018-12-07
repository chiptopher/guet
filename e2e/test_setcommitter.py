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
from os.path import join, expanduser

from e2e.e2etest import E2ETest
from guet import constants as const
from guet.gateways.gateway import PairSetGatewayCommitterGateway


class TestGuetSet(E2ETest):

    def test_set_committers_creates_a_pair_set_for_the_users(self):
        process = subprocess.Popen(['guet', 'init'])
        process.wait()
        process = subprocess.Popen(['guet', 'add', 'initials1', 'name1', 'email1@localhost'])
        process.wait()
        process = subprocess.Popen(['guet', 'add', 'initials2', 'name2', 'email2@localhost'])
        process.wait()
        process = subprocess.Popen(['guet', 'set', 'initials1', 'initials2'])
        process.wait()
        pair_set_committer_gateway = PairSetGatewayCommitterGateway()
        self.assertEqual('initials1', pair_set_committer_gateway.get_pair_set_committers_by_pair_set_id(1)[0].committer_initials)
        self.assertEqual('initials2', pair_set_committer_gateway.get_pair_set_committers_by_pair_set_id(1)[1].committer_initials)

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

        with open(join(expanduser('~'), const.APP_FOLDER_NAME, const.AUTHOR_EMAIL)) as auther_email:
            content = auther_email.readline()
        self.assertEqual(email, content)

        with open(join(expanduser('~'), const.APP_FOLDER_NAME, const.AUTHOR_NAME)) as auther_name:
            content = auther_name.readline()
        self.assertEqual(name, content)

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

    def test_set_gracefully_displays_error_message_when_setting_committer_with_unknown_initials(self):
        process = subprocess.Popen(['guet', 'init'])
        process.wait()
        process = subprocess.Popen(['guet', 'set', 'ui'], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        full_output = process.communicate()
        output = full_output[0].decode('utf-8')
        self.assertEqual("No committer exists with initials 'ui'\n", output)
