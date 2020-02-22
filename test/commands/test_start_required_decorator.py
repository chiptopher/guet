from unittest import TestCase
from unittest.mock import Mock, patch

from guet.commands.print_strategy import PrintCommandStrategy
from guet.commands.start_required_decorator import StartRequiredDecorator
from guet.settings.settings import Settings


@patch('guet.commands.start_required_decorator.git_path_from_cwd')
@patch('guet.commands.start_required_decorator.Git')
class TestStartRequiredDecorator(TestCase):
    def test_calls_decorated_build(self, mock_git, mock_git_path_from_cwd):
        mock_command = Mock()
        mock_factory = Mock()
        mock_factory.build.return_value = mock_command
        decorator = StartRequiredDecorator(mock_factory)
        self.assertEqual(mock_command, decorator.build([], Settings()))

    def test_returns_command_with_print_strategy_with_error_message(self, mock_git, mock_git_path_from_cwd):
        decorator = StartRequiredDecorator(Mock())
        mock_git.return_value.hooks_present.return_value = False
        command = decorator.build([], Settings())

        self.assertIsInstance(command.strategy, PrintCommandStrategy)