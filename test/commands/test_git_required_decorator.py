from unittest import TestCase
from unittest.mock import Mock, patch

from guet.commands.git_required_decorator import GitRequiredDecorator
from guet.commands.print_strategy import PrintCommandStrategy
from guet.settings.settings import Settings


@patch('guet.commands.git_required_decorator.git_present_in_cwd', return_value=True)
class TestGitRequiredDecorator(TestCase):

    def test_returns_decorated_factory_build(self, _):
        mock_command = Mock()
        mock_factory = Mock()
        mock_factory.build.return_value = mock_command

        decorator = GitRequiredDecorator(mock_factory)

        result = decorator.build([], Settings())
        self.assertEqual(mock_command, result)

    def test_does_not_build_decorated_factory_when_git_not_present_in_cwd(self, mock_git_present_in_cwd):
        mock_git_present_in_cwd.return_value = False

        mock_command = Mock()
        mock_factory = Mock()
        mock_factory.build.return_value = mock_command

        decorator = GitRequiredDecorator(mock_factory)

        decorator.build([], Settings())
        mock_factory.build.assert_not_called()

    def test_returns_command_with_print_strategy_that_says_git_not_present_in_cwd(self, mock_git_present_in_cwd):
        mock_git_present_in_cwd.return_value = False

        mock_command = Mock()
        mock_factory = Mock()
        mock_factory.build.return_value = mock_command

        decorator = GitRequiredDecorator(mock_factory)

        result = decorator.build([], Settings())
        self.assertIsInstance(result.strategy, PrintCommandStrategy)
        self.assertEqual(result.strategy._text, 'Git not initialized in this directory.')
