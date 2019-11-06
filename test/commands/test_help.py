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

from unittest.mock import Mock, patch

from guet.commands.command import Command
from guet.commands.help import HelpCommand
from test.commands.test_command import CommandTest, create_test_case


class TestHelpCommand(CommandTest):

    @patch('builtins.print')
    def test_execute_raises_not_implemented_error(self, mock_print):

        class MockCommand(Command):
            def help(self):
                raise NotImplementedError

        class MockCommandA(MockCommand):
            def help(self):
                return 'Mock command A'

        command = HelpCommand([])
        command.execute()
        mock_print.assert_called_once()

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

        help_command = HelpCommand(None)
        actual = help_command.help(lambda ignored_commands: [MockCommandA])
        expected = 'usage: guet <command>\n\n   MockCommandA -- Mock command A\n'
        self.assertEqual(expected, actual)
