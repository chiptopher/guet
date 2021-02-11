from unittest import TestCase
from unittest.mock import Mock, call, patch

from guet.commands.set._set_committers import SetCommittersAction
from guet.committers.committer import Committer


class TestSetCommittersAction(TestCase):
    def test_execute_sets_committers(self):
        current_committers = Mock()
        committers = Mock()
        action = SetCommittersAction(committers, current_committers)

        committer = Committer('name', 'email', 'first')
        committers.all.return_value = [committer]

        action.execute(['first'])

        current_committers.set.assert_called_with([committer])

    def test_execute_ignores_committers_not_in_args(self):
        current_committers = Mock()
        committers = Mock()
        action = SetCommittersAction(committers, current_committers)

        first = Committer('name', 'email', 'first')
        second = Committer('name', 'email', 'second')
        committers.all.return_value = [first, second]

        action.execute(['first'])

        current_committers.set.assert_called_with([first])

    @patch('builtins.print')
    def test_execute_prints_set_committers(self, mock_print):
        current_committers = Mock()
        committers = Mock()
        action = SetCommittersAction(committers, current_committers)

        first = Committer('name', 'email', 'first')
        second = Committer('name', 'email', 'second')
        committers.all.return_value = [first, second]

        action.execute(['first'])

        mock_print.assert_has_calls([
            call('Committers set to:'),
            call('first - name <email>')
        ])

    def test_execute_ignores_case_when_finding_committers(self):
        current_committers = Mock()
        committers = Mock()
        action = SetCommittersAction(committers, current_committers)

        first = Committer('name', 'email', 'first')
        second = Committer('name', 'email', 'second')
        committers.all.return_value = [first, second]

        action.execute(['first', 'SECOND'])

        current_committers.set.assert_called_with([first, second])
