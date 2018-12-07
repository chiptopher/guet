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

from unittest.mock import Mock

from guet.commands.init import InitDataSourceCommand
from guet.gateways.gateway import *
from guet.gateways.io import PrintGateway
from test.commands.test_command import CommandTest, create_test_case


class TestInitDataSourceCommand(CommandTest):

    def test_execute_uses_gateway_to_create_data_source(self):

        file_gateway = FileGateway()
        file_gateway.initialize = Mock()
        file_gateway.path_exists = Mock(return_value=False)

        command = InitDataSourceCommand(['init'], file_gateway)
        command.execute()

        file_gateway.initialize.assert_called()

    def test_validate(self):

        cases = [
            create_test_case(['init'], True, 'Init requires first command'),
            create_test_case([], False, 'Should return false when there are too few arguments'),
            create_test_case(['wrong'], False, 'Should return false when the required arg is wrong'),
            create_test_case(['init', 'extra'], True, 'Should return true when there are extra commands')
        ]

        for case in cases:
            self._validate_test(case, InitDataSourceCommand([]))

    def test_validate_just_init_returns_true(self):
        self.assertTrue(InitDataSourceCommand.validate(['init']))

    def test_execute_prints_out_error_message_when_calling_init_when_it_has_already_been_called(self):

        file_gateway = FileGateway()
        file_gateway.initialize = Mock()
        path_exists_mock = Mock()
        path_exists_mock.return_value = False
        file_gateway.path_exists = path_exists_mock

        print_gateway = PrintGateway()
        print_gateway.print = Mock()

        command = InitDataSourceCommand(['init'], file_gateway, print_gateway)
        command.execute()
        path_exists_mock.return_value = True
        command.execute()

        file_gateway.initialize.assert_called_once()
        print_gateway.print.assert_called_once_with('Config folder already exists.')

    def test_execute_prints_help_command_when_there_are_incorrect_arguments(self):

        file_gateway = FileGateway()
        file_gateway.initialize = Mock()
        path_exists_mock = Mock()
        path_exists_mock.return_value = False
        file_gateway.path_exists = path_exists_mock

        print_gateway = PrintGateway()
        print_gateway.print = Mock()

        command = InitDataSourceCommand(['init', 'invalid arg'], file_gateway, print_gateway)
        command.execute()
        print_gateway.print.assert_called_with('Invalid arguments.\n\n   {}'.format(command.help()))

    def test_get_short_help_message(self):

        self.assertEqual('Initialize guet for use', InitDataSourceCommand.get_short_help_message())
