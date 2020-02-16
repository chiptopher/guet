import unittest
from unittest.mock import Mock

from guet.commands.command_factory import CommandFactoryMethod
from guet.commands.help.guet_usage import guet_usage


class TestHelpCommand(unittest.TestCase):
    def test_help_message_consists_of_all_commands_help_messages_of_commands_passed_to_map(self):
        mock_command_factory = CommandFactoryMethod()
        mock_command_factory.short_help_message = Mock(return_value='Mock Command B')

        command_builder_map = dict()
        command_builder_map['MockCommandB'] = mock_command_factory

        actual = guet_usage(command_builder_map)
        expected = 'usage: guet <command>\n\n   MockCommandB -- Mock Command B\n'
        self.assertEqual(expected, actual)
