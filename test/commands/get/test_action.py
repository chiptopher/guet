from unittest import TestCase
from unittest.mock import Mock, call, patch

from guet.commands.get._action import GetCommittersAction
from guet.committers.committer import Committer


@patch('builtins.print')
class TestGetCommittersAction(TestCase):

    def test_prints_list_of_committers(self, mock_print):
        committers = Mock()
        action = GetCommittersAction(committers, Mock())

        committers.all = Mock(return_value=[
            Committer('name1', 'email1', 'initials1'),
            Committer('name2', 'email2', 'initials2'),
        ])

        action.execute(['all'])

        mock_print.assert_has_calls([
            call('All committers'),
            call('initials1 - name1 <email1>'),
            call('initials2 - name2 <email2>'),
        ])

    def test_prints_list_of_currently_set_committers(self, mock_print):
        current = Mock()
        action = GetCommittersAction(Mock(), current)

        current.get = Mock(return_value=[
            Committer('name1', 'email1', 'initials1'),
            Committer('name2', 'email2', 'initials2'),
        ])

        action.execute(['current'])

        mock_print.assert_has_calls([
            call('Current committers'),
            call('initials1 - name1 <email1>'),
            call('initials2 - name2 <email2>'),
        ])
