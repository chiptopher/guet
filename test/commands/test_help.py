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

from test.commands.test_command import CommandTest, create_test_case
from guet.commands.help import HelpCommand
from guet.commands.command import Command
from guet.gateway import *
from unittest.mock import Mock
from guet import commands
import importlib
import inspect


class TestHelpCommand(CommandTest):

    def test_validate(self):

        cases = [
            create_test_case([], False, 'Should return false when there are no arguments'),
            create_test_case(['one'], False, 'Should return false when there is one argument'),
            create_test_case(['one', 'two'], False, 'Should return false when there are more than one arguments'),
        ]

        for case in cases:
            self._validate_test(case, HelpCommand([]))

    def test_init(self):
        mock_print_gateway = PrintGateway(None)
        command = HelpCommand([], mock_print_gateway)
        self.assertEqual(mock_print_gateway, command._print_gateway)

    def test_execute_raises_not_implemented_error(self):
        mock_print_gateway = PrintGateway(None)
        mock_print_gateway.print = Mock()

        class MockCommand(Command):
            def help(self):
                raise NotImplementedError

        class MockCommandA(MockCommand):
            def help(self):
                return 'Mock command A'

        command = HelpCommand([], mock_print_gateway)
        command.execute()
        mock_print_gateway.print.assert_called_once()

    def test_help_message_consists_of_all_commands_help_messages(self):

        class MockCommand(Command):

            def get_short_help_message(self):
                raise NotImplementedError

            def get_list_of_required_arguments_in_correct_order(cls):
                raise NotImplementedError

        class MockCommandA(MockCommand):
            @classmethod
            def get_list_of_required_arguments_in_correct_order(cls):
                return ['MockCommandA']

            @classmethod
            def get_short_help_message(cls):
                return 'Mock command A'

        mock_print_gateway = PrintGateway(None)
        mock_print_gateway.print = Mock()

        help_command = HelpCommand(None, mock_print_gateway)
        actual = help_command.help(lambda ignored_commands: [MockCommandA])
        expected = 'usage: guet <command>\n\n   MockCommandA -- Mock command A\n'
        self.assertEqual(expected, actual)
