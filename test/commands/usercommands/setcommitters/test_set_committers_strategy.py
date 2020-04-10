from unittest import TestCase
from unittest.mock import patch, Mock

from guet.commands.usercommands.setcommitters.set_committers_strategy import SetCommittersStrategy
from guet.committers.committer import Committer
from guet.context.context import Context


class TestSetCommittersStrategy(TestCase):

    def test_apply_set_commiters_with_context(self):
        mock_context = Mock()
        mock_committers = Mock()
        mock_context.committers = mock_committers
        committer1 = Committer(name='name1', email='email1', initials='initials1')
        committer2 = Committer(name='name2', email='email2', initials='initials2')
        mock_committers.all.return_value = [committer1, committer2]

        strategy = SetCommittersStrategy(['initials1', 'initials2'], mock_context)
        strategy.apply()

        mock_context.set_committers.assert_called_with([committer1, committer2])

    @patch('builtins.print')
    def test_execute_prints_out_error_message_when_the_given_initials_arent_in_the_system(self, mock_print):
        mock_context = Mock()
        mock_committers = Mock()
        mock_context.committers = mock_committers
        mock_committers.all.return_value = [Committer('undesired', 'undesired', 'undesired')]
        strategy = SetCommittersStrategy(['initials'], mock_context)
        strategy.apply()
        mock_print.assert_called_once_with("No committer exists with initials 'initials'")

    def test_execute_failing_doesnt_set_committers_still(self):
        mock_context = Mock()
        mock_committers = Mock()
        mock_context.committers = mock_committers
        mock_committers.all.return_value = [Committer('undesired', 'undesired', 'undesired')]
        strategy = SetCommittersStrategy(['initials'], mock_context)
        strategy.apply()
        context: Context = mock_context.return_value
        context.notify_set_committer_observers.assert_not_called()
