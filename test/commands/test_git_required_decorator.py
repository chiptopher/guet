from os.path import join
from unittest import TestCase
from unittest.mock import Mock, patch

from guet.commands.git_required_decorator import GitRequiredDecorator
from guet.commands.print_strategy import PrintCommandStrategy
from guet.git.errors import NoGitPresentError
from guet.settings.settings import Settings


@patch('guet.commands.git_required_decorator.Git')
@patch('guet.commands.git_required_decorator.getcwd', return_value='/absolute/path/to/cwd')
class TestGitRequiredDecorator(TestCase):

    def test_returns_decorated_factory_build(self, _1, _2):
        mock_command = Mock()
        mock_factory = Mock()
        mock_factory.build.return_value = mock_command

        decorator = GitRequiredDecorator(mock_factory)

        result = decorator.build([], Settings())
        self.assertEqual(mock_command, result)

    def test_does_not_build_decorated_factory_when_git_not_present_in_cwd(self, mock_getcwd, mock_git):
        mock_git.side_effect = NoGitPresentError()

        mock_command = Mock()
        mock_factory = Mock()
        mock_factory.build.return_value = mock_command

        decorator = GitRequiredDecorator(mock_factory)

        decorator.build([], Settings())
        mock_factory.build.assert_not_called()

    def test_returns_command_with_print_strategy_that_says_git_not_present_in_cwd(self, mock_getcwd, mock_git):
        mock_git.side_effect = NoGitPresentError()

        mock_command = Mock()
        mock_factory = Mock()
        mock_factory.build.return_value = mock_command

        decorator = GitRequiredDecorator(mock_factory)

        result = decorator.build([], Settings())
        self.assertIsInstance(result.strategy, PrintCommandStrategy)
        self.assertEqual(result.strategy._text, 'Git not initialized in this directory.')

    def test_build_loads_git_from_cwd(self, mock_getcwd, mock_git):
        cwd_path = '/absolute/path/to/cwd'
        mock_getcwd.return_value = cwd_path
        mock_command = Mock()
        mock_factory = Mock()
        mock_factory.build.return_value = mock_command

        decorator = GitRequiredDecorator(mock_factory)

        decorator.build([], Settings())

        mock_git.assert_called_with(join(cwd_path, '.git'))
