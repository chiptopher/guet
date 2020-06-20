from unittest import TestCase
from unittest.mock import patch, Mock

from guet.commands.usercommands.start._create_alongside_hook_strategy import CreateAlongsideHookAction


class TestCreateAlongsideHookStrategy(TestCase):

    def test_creates_hooks_with_alongside_mode(self):
        context = Mock()
        context.git = Mock()
        strategy = CreateAlongsideHookAction(context.git)
        strategy.apply()
        context.git.create_hooks.assert_called_with(alongside=True)
