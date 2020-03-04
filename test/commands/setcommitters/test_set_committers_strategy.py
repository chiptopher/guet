from unittest import TestCase
from unittest.mock import patch

from guet.commands.setcommitters.set_committers_strategy import SetCommittersStrategy
from guet.config.committer import Committer
from guet.context.context import Context


@patch('guet.commands.setcommitters.set_committers_strategy.getcwd', return_value='/path/to/cwd')
@patch('guet.commands.setcommitters.set_committers_strategy.Context')
@patch('guet.commands.setcommitters.set_committers_strategy.get_committers')
class TestSetCommittersStrategy(TestCase):

    def test_apply_set_commiters_with_context(self, mock_get_committers, mock_context, mock_getcwd):
        committer1 = Committer(name='name1', email='email1', initials='initials1')
        committer2 = Committer(name='name2', email='email2', initials='initials2')
        mock_get_committers.return_value = [committer1, committer2]

        strategy = SetCommittersStrategy(['initials1', 'initials2'])
        strategy.apply()

        context: Context = mock_context.return_value
        context.set_committers.assert_called_with([committer1, committer2])

    @patch('builtins.print')
    def test_execute_prints_out_error_message_when_the_given_initials_arent_in_the_system(
            self, mock_print, mock_get_committers, mock_context, mock_getcwd):
        mock_get_committers.return_value = [Committer('undesired', 'undesired', 'undesired')]
        strategy = SetCommittersStrategy(['initials'])
        strategy.apply()
        mock_print.assert_called_once_with("No committer exists with initials 'initials'")

    def test_execute_failing_doesnt_set_committers_still(self, mock_get_committers, mock_context, mock_getcwd):
        mock_get_committers.return_value = [Committer('undesired', 'undesired', 'undesired')]
        strategy = SetCommittersStrategy(['initials'])
        strategy.apply()
        context: Context = mock_context.return_value
        context.notify_set_committer_observers.assert_not_called()
