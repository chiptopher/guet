from unittest import TestCase
from unittest.mock import Mock, patch, call

from guet.commands.set._set_committers import SetCommittersAction
from guet.committers.committer import Committer


class TestSetCommittersAction(TestCase):
    def test_execute_sets_committers(self):
        context = Mock()
        committers = Mock()
        action = SetCommittersAction(committers, context)

        committer = Committer('name', 'email', 'first')
        committers.all.return_value = [committer]

        action.execute(['first'])

        context.set_committers.assert_called_with([committer])

    def test_execute_ignores_committers_not_in_args(self):
        context = Mock()
        committers = Mock()
        action = SetCommittersAction(committers, context)

        first = Committer('name', 'email', 'first')
        second = Committer('name', 'email', 'second')
        committers.all.return_value = [first, second]

        action.execute(['first'])

        context.set_committers.assert_called_with([first])

    @patch('builtins.print')
    def test_execute_prints_set_committers(self, mock_print):
        context = Mock()
        committers = Mock()
        action = SetCommittersAction(committers, context)

        first = Committer('name', 'email', 'first')
        second = Committer('name', 'email', 'second')
        committers.all.return_value = [first, second]

        action.execute(['first'])

        mock_print.assert_has_calls([
            call('Committers set to:'),
            call('first - name <email>')
        ])

    def test_execute_ignores_case_when_finding_committers(self):
        context = Mock()
        committers = Mock()
        action = SetCommittersAction(committers, context)

        first = Committer('name', 'email', 'first')
        second = Committer('name', 'email', 'second')
        committers.all.return_value = [first, second]

        action.execute(['first', 'SECOND'])

        context.set_committers.assert_called_with([first, second])
