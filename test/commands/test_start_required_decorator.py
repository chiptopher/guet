from unittest import TestCase
from unittest.mock import Mock, patch

from guet.commands.print_strategy import PrintCommandStrategy
from guet.commands.start_required_decorator import StartRequiredDecorator, NOT_RAN_IN_ROOT_DIRECTORY_ERROR
from guet.git.errors import NoGitPresentError
from guet.settings.settings import Settings


@patch('guet.commands.start_required_decorator.project_root')
@patch('guet.commands.start_required_decorator.Git')
class TestStartRequiredDecorator(TestCase):
    def test_calls_decorated_build(self, mock_git, mock_project_root):
        mock_command = Mock()
        mock_factory = Mock()
        mock_factory.build.return_value = mock_command
        decorator = StartRequiredDecorator(mock_factory)
        self.assertEqual(mock_command, decorator.build([], Settings()))

    def test_returns_command_with_print_strategy_with_error_message(self, mock_git, mock_project_root):
        decorator = StartRequiredDecorator(Mock())
        mock_git.return_value.hooks_present.return_value = False
        command = decorator.build([], Settings())

        self.assertIsInstance(command.strategy, PrintCommandStrategy)

    def test_returns_error_message_when_no_git_present(self, mock_git, mock_project_root):
        mock_git.side_effect = FileNotFoundError()
        decorator = StartRequiredDecorator(Mock())
        command = decorator.build([], Settings())

        self.assertIsInstance(command.strategy, PrintCommandStrategy)
        self.assertEqual(NOT_RAN_IN_ROOT_DIRECTORY_ERROR, command.strategy._text)
