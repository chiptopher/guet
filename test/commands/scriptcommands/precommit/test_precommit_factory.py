from unittest import TestCase
from unittest.mock import patch, Mock

from guet.commands.strategies.error_strategy import ErrorStrategy
from guet.config.committer import Committer

from guet.commands.strategies.strategy_command import StrategyCommand
from guet.settings.settings import Settings

from guet.commands.scriptcommands.precommit.precommit_factory import PreCommitFactory, \
    NO_COMMITTERS_SET_ERROR_MESSAGE


@patch('guet.commands.command_factory.Context')
class PreCommitFactoryTest(TestCase):

    def test_returns_error_message_strategy_if_no_current_committers(self, mock_context):
        mock_context_instance = Mock()
        mock_context_instance.committers = Mock()
        mock_context_instance.committers.current.return_value = []

        mock_context.instance.return_value = mock_context_instance
        factory = PreCommitFactory()
        command: StrategyCommand = factory.build([], Settings())

        self.assertIsInstance(command.strategy, ErrorStrategy)
        self.assertEqual(command.strategy.error_message, NO_COMMITTERS_SET_ERROR_MESSAGE)

    @patch('guet.commands.scriptcommands.precommit.precommit_factory.PreCommitStrategy')
    def test_returns_pre_commit_strategy_if_there_are_currently_set_committers(self, mock_precommit_strategy,
                                                                               mock_context):
        mock_context_instance = Mock()
        mock_context_instance.committers = Mock()
        mock_context_instance.committers.current.return_value = [
            Committer('name1', 'email1', 'initials1'),
            Committer('name2', 'email2', 'initials2')
        ]

        mock_context.instance.return_value = mock_context_instance
        factory = PreCommitFactory()
        command: StrategyCommand = factory.build([], Settings())

        self.assertEqual(command.strategy, mock_precommit_strategy.return_value)
