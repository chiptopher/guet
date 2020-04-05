from unittest import TestCase
from unittest.mock import Mock, patch

from guet.commands.usercommands.remove.remove_strategy import RemoveCommitterStrategy
from guet.config.committer import Committer
from guet.config.errors import InvalidInitialsError
from guet.context.context import Context


class TestRemoveCommitterStrategy(TestCase):

    def test_apply_removes_committer(self):
        committer1 = Committer(name='name1', email='email1', initials='initials1')
        committer2 = Committer(name='name2', email='email2', initials='initials2')

        committers = Mock()
        committers.all.return_value = [committer1, committer2]
        committers.by_initials.return_value = committer1

        context: Context = Mock()
        context.committers = committers

        strategy = RemoveCommitterStrategy('initials1', context)
        strategy.apply()

        committers.by_initials.assert_called_with('initials1')
        committers.remove.assert_called_with(committer1)

    @patch('builtins.print')
    def test_apply_prints_error_message_if_no_committers_exists_with_given_initials(self, mock_print):
        committers = Mock()
        committers.all.return_value = []
        committers.by_initials.side_effect = InvalidInitialsError()

        context: Context = Mock()
        context.committers = committers

        strategy = RemoveCommitterStrategy('initials1', context)
        strategy.apply()

        mock_print.assert_called_with('No committer exists with initials "initials1"')
