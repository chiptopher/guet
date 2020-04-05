from unittest import TestCase
from unittest.mock import MagicMock

from guet.commands.strategies.strategy_command import StrategyCommand
from guet.commands.strategies.strategy import CommandStrategy


class TestStrategyCommand(TestCase):

    def test_execute_calls_the_strategy_apply(self):
        strategy = MagicMock(CommandStrategy)
        strategy.apply = MagicMock()
        command = StrategyCommand(strategy)
        command.execute()
        strategy.apply.assert_called_once()
