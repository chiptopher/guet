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
import unittest

from guet.commands.command import Command
from guet.commands.help import HelpCommand


class TestHelpCommand(unittest.TestCase):

    def test_help_message_consists_of_all_commands_help_messages(self):

        class MockCommand(Command):

            def get_short_help_message(self):
                raise NotImplementedError

            def get_list_of_required_arguments_in_correct_order(cls):
                raise NotImplementedError

        class MockCommandA(MockCommand):

            @classmethod
            def get_short_help_message(cls):
                return 'Mock command A'

        command_builder_map = dict()
        command_builder_map['MockCommandA'] = MockCommandA
        help_command = HelpCommand([], command_builder_map)
        actual = help_command.help()
        expected = 'usage: guet <command>\n\n   MockCommandA -- Mock command A\n'
        self.assertEqual(expected, actual)
