from unittest import TestCase
from unittest.mock import patch

from guet.commands.scriptcommands.commitmsg.commitmsg_strategy import CommitMsgStrategy
from guet.commands.strategies.strategy_command import StrategyCommand
from guet.settings.settings import Settings

from guet.commands.scriptcommands.commitmsg.commitmsg_factory import CommitMsgFactory


@patch('guet.commands.scriptcommands.commitmsg.commitmsg_factory.CommitMsgStrategy')
@patch('guet.commands.command_factory.Context')
class TestCommitMsgFactory(TestCase):

    def test_build_retruns_commit_msg_strategy(self, mock_context, mock_commitmsg_strategy):
        factory = CommitMsgFactory()
        command: StrategyCommand = factory.build([], Settings())

        self.assertEqual(command.strategy, mock_commitmsg_strategy.return_value)
        mock_commitmsg_strategy.assert_called_with(mock_context.instance.return_value)
