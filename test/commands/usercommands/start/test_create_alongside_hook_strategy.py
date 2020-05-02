from unittest import TestCase
from unittest.mock import patch, Mock

from guet.commands.usercommands.start.create_alongside_hook_strategy import CreateAlongsideHookStrategy


class TestCreateAlongsideHookStrategy(TestCase):

    def test_creates_hooks_with_alongside_mode(self):
        context = Mock()
        context.git = Mock()
        strategy = CreateAlongsideHookStrategy(context.git)
        strategy.apply()
        context.git.create_hooks.assert_called_with(alongside=True)
