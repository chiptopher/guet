import unittest
from unittest.mock import Mock

from guet.commands.argsettingcommand import ArgSettingCommand
from guet.commands.command_factory import CommandFactoryMethod
from guet.settings.settings import Settings
from guet.commands.help.guet_usage import guet_usage


class TestHelpCommand(unittest.TestCase):
    def test_help_message_consists_of_all_commands_help_messages_of_commands_passed_to_map(self):
        class MockCommandA(ArgSettingCommand):
            @classmethod
            def get_short_help_message(cls):
                return 'Mock command A'

        mock_command_factory = CommandFactoryMethod()
        mock_command_factory.short_help_message = Mock(return_value='Mock Command B')

        command_builder_map = dict()
        command_builder_map['MockCommandA'] = MockCommandA
        command_builder_map['MockCommandB'] = mock_command_factory

        actual = guet_usage(command_builder_map)
        expected = 'usage: guet <command>\n\n   MockCommandA -- Mock command A\n   MockCommandB -- Mock Command B\n'
        self.assertEqual(expected, actual)
