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
from guet.gateway import UserGateway
from guet.commands.addcommitter import AddUserCommand
import subprocess


class TestAddUser(E2ETest):

    def test_add_committer(self):
        process = subprocess.Popen(['guet', 'init'])
        process.wait()
        initials = 'usr'
        name = 'User McUser'
        email = 'usr@localhost'
        process = subprocess.Popen(['guet', 'add', initials, name, email])
        process.wait()
        user_gateway = UserGateway()
        user = user_gateway.get_user(initials)
        self.assertEqual(user.email, email)
        self.assertEqual(user.name, name)

    def test_add_committer_overwrites_existing_committer(self):
        process = subprocess.Popen(['guet', 'init'])
        process.wait()
        initials = 'usr'
        name = 'User McUser'
        email = 'usr@localhost'
        process = subprocess.Popen(['guet', 'add', initials, name, email])
        process.wait()
        new_name = 'New Name'
        process = subprocess.Popen(['guet', 'add', initials, new_name, email])
        process.wait()
        user_gateway = UserGateway()
        user = user_gateway.get_user(initials)
        self.assertEqual(user.name, new_name)

    def test_add_committer_too_many_arguments_prints_error_message(self):
        process = subprocess.Popen(['guet', 'init'])
        process.wait()
        initials = 'usr'
        name = 'User McUser'
        email = 'usr@localhost'
        process = subprocess.Popen(['guet', 'add', initials, name, email, 'exta'], stdout=subprocess.PIPE)
        process.wait()
        self.assertEqual('Too many arguments.\n', self._parse_output(process))
        process.stdout.close()

    def test_add_committer_not_enough_args_prints_the_error_message_and_help_for_command(self):
        process = subprocess.Popen(['guet', 'init'])
        process.wait()
        initials = 'usr'
        name = 'User McUser'
        process = subprocess.Popen(['guet', 'add', initials, name], stdout=subprocess.PIPE)
        process.wait()
        expected = 'Not enough arguments.\n\n{}\n\n'.format(AddUserCommand([]).help())
        self.assertEqual(expected, self._parse_output(process))
        process.stdout.close()
