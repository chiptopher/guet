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

from unittest.mock import Mock, call

from guet.commands.addcommitter import AddUserCommand
from guet.gateways.gateway import *
from guet.gateways.io import PrintGateway
from test.commands.test_command import CommandTest, create_test_case


class TestAddUserCommand(CommandTest):

    def test_validate(self):
        cases = [
            create_test_case(['add'], True, 'Should return true with correct number of args'),
            create_test_case(['add', 'extra'], True, 'Should return true when there are extra arguments'),
            create_test_case(['wrong'], False, 'Should return false when the required args are wrong'),
            create_test_case([], False, 'Should return false when there are not enough args')
        ]

        for case in cases:
            self._validate_test(case, AddUserCommand)

    def test_execute_calls_add_user(self):

        mock_user_gateway = UserGateway()
        mock_user_gateway.add_user = Mock()

        initials = 'usr'
        name = 'user'
        email = 'user@localhost'
        command = AddUserCommand(['guet', initials, name, email], mock_user_gateway)
        command.execute()
        mock_user_gateway.add_user.assert_called_once_with(initials, name, email)

    def test_execute_prints_error_message_when_too_many_arguments_are_given(self):

        mock_user_gateway = UserGateway()
        mock_user_gateway.add_user = Mock()

        mock_print_gateway = PrintGateway()
        mock_print_gateway.print = Mock()

        initials = 'usr'
        name = 'user'
        email = 'user@localhost'
        command = AddUserCommand(['guet', initials, name, email, 'extra'], mock_user_gateway, mock_print_gateway)
        command.execute()

        mock_print_gateway.print.assert_called_once_with('Too many arguments.')

    def test_execute_prints_the_error_message_and_help_message_when_there_are_not_enough_args(self):

        mock_user_gateway = UserGateway()
        mock_user_gateway.add_user = Mock()

        mock_print_gateway = PrintGateway()
        mock_print_gateway.print = Mock()

        command = AddUserCommand(['guet', 'initials', 'name'], mock_user_gateway, mock_print_gateway)
        command.execute()

        calls = [call('Not enough arguments.'), call(''), call(command.help())]
        mock_print_gateway.print.assert_has_calls(calls)

    def test_help_prints_the_help_message(self):

        command = AddUserCommand([])
        self.assertEqual('usage: guet add <initials> <"name"> <email>', command.help())

    def test_get_short_help_message(self):
        self.assertEqual('Add committer to the list of available committers', AddUserCommand.get_short_help_message())
