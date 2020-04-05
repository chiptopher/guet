from unittest import TestCase
from unittest.mock import patch, Mock

from guet.commands.usercommands.start.create_alongside_hook_strategy import CreateAlongsideHookStrategy


class TestCreateAlongsideHookStrategy(TestCase):

    @patch('guet.commands.usercommands.start.create_alongside_hook_strategy.Git')
    def test_creates_hooks_with_alongside_mode(self, mock_git):
        hooks_path = '/path/to/.git/hooks'
        strategy = CreateAlongsideHookStrategy(hooks_path, Mock())
        strategy.apply()
        mock_git.assert_called_with('/path/to/.git')
        mock_git.return_value.create_hooks.assert_called_with(alongside=True)
