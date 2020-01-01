from unittest import TestCase
from unittest.mock import Mock, patch

from guet.commands.command import Command
from guet.commands.command_factory import CommandFactoryMethod
from guet.commands.help_decorator import HelpDecorator
from guet.settings.settings import Settings


@patch('builtins.print')
class TestHelpDecorator(TestCase):

    def test_returns_command_from_wrapped_builder(self, mock_print):
        mock_command = Mock(Command())
        mock_factory = Mock(CommandFactoryMethod())
        mock_factory.build = Mock(return_value=mock_command)

        help_decorator = HelpDecorator(mock_factory, "help message")
        command = help_decorator.build(["command", "arg"], Settings())
        self.assertEqual(command, mock_command)

    def test_returns_command_that_prints_help_message_if_no_args_are_given_other_than_command_name(self, mock_print):
        mock_command = Mock(Command())
        mock_factory = Mock(CommandFactoryMethod())
        mock_factory.build = Mock(return_value=mock_command)

        help_decorator = HelpDecorator(mock_factory, "help message")
        command = help_decorator.build(["command"], Settings())
        command.execute()

        mock_print.assert_called_with('help message')

    def test_returns_command_that_prints_help_message_if_there_is_a_dash_help_in_args(self, mock_print):
        mock_command = Mock(Command())
        mock_factory = Mock(CommandFactoryMethod())
        mock_factory.build = Mock(return_value=mock_command)

        help_decorator = HelpDecorator(mock_factory, "help message")
        command = help_decorator.build(["command", '--help'], Settings())
        command.execute()

        mock_print.assert_called_with('help message')

    def test_returns_command_that_prints_help_message_if_there_is_a_dash_h_in_args(self, mock_print):
        mock_command = Mock(Command())
        mock_factory = Mock(CommandFactoryMethod())
        mock_factory.build = Mock(return_value=mock_command)

        help_decorator = HelpDecorator(mock_factory, "help message")
        command = help_decorator.build(["command", '-h'], Settings())
        command.execute()

        mock_print.assert_called_with('help message')

    def test_returns_decorated_if_no_args_valid_set_to_true(self, mock_print):
        mock_command = Mock(Command())
        mock_factory = Mock(CommandFactoryMethod())
        mock_factory.build = Mock(return_value=mock_command)

        help_decorator = HelpDecorator(mock_factory, "help message", no_args_valid=True)
        command = help_decorator.build(["command"], Settings())
        command.execute()

        mock_print.assert_not_called()
