from unittest import TestCase
from unittest.mock import patch, call

from guet.commands.start.create_alongside_hook_strategy import CreateAlongsideHookStrategy
from guet.git.create_hook import Hooks
from guet.git.hook_mode import HookMode


class TestCreateAlongsideHookStrategy(TestCase):

    @patch('guet.commands.start.create_alongside_hook_strategy.create_hook')
    def test_creates_hooks_with_alongside_mode(self, mock_create_hook):
        strategy = CreateAlongsideHookStrategy('/path')
        strategy.apply()
        mock_create_hook.assert_has_calls([
            call('/path', Hooks.PRE_COMMIT, HookMode.CREATE_ALONGSIDE),
            call('/path', Hooks.POST_COMMIT, HookMode.CREATE_ALONGSIDE),
            call('/path', Hooks.COMMIT_MSG, HookMode.CREATE_ALONGSIDE)
        ])
