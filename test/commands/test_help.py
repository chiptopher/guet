
import unittest

from guet.commands.command import Command
from guet.commands.help import HelpCommand
from guet.settings.settings import Settings


class TestHelpCommand(unittest.TestCase):

    def test_help_message_consists_of_all_commands_help_messages(self):

        class MockCommand(Command):

            def get_short_help_message(self):
                raise NotImplementedError

            def get_list_of_required_arguments_in_correct_order(self):
                raise NotImplementedError

        class MockCommandA(MockCommand):

            @classmethod
            def get_short_help_message(cls):
                return 'Mock command A'

        command_builder_map = dict()
        command_builder_map['MockCommandA'] = MockCommandA
        help_command = HelpCommand([], Settings(), command_builder_map)
        actual = help_command.help()
        expected = 'usage: guet <command>\n\n   MockCommandA -- Mock command A\n'
        self.assertEqual(expected, actual)
