from unittest import TestCase
from unittest.mock import patch

from guet.config.committer import Committer
from guet.commands.get import GetCommand
from guet.settings.settings import Settings


@patch('guet.commands.get.get_committers')
@patch('guet.commands.get.get_current_committers')
@patch('builtins.print')
class GetCommandTest(TestCase):
    def test_execute_lists_current_committers_when_given_current_arg(self, mock_print,
                                                                     mock_get_current_committers,
                                                                     mock_get_committers):
        mock_get_current_committers.return_value = [
            Committer('name1', 'email1', 'initials1'),
            Committer('name2', 'email2', 'initials2')
        ]
        command = GetCommand(['get', 'current'], Settings())
        command.execute()
        mock_print.assert_any_call('initials1 - name1 <email1>')
        mock_print.assert_any_call('initials2 - name2 <email2>')

    def test_prints_error_message_when_given_invalid_get(self, mock_print,
                                                         mock_get_current_committers,
                                                         mock_get_committers):
        command = GetCommand(['get', 'invalid'], Settings())
        command.execute()
        mock_print.assert_any_call('Invalid identifier <invalid>')

    def test_execute_lists_all_commits_when_given_committers_arg(self, mock_print,
                                                                 mock_get_current_committers,
                                                                 mock_get_committers):
        mock_get_committers.return_value = [
            Committer('name1', 'email1', 'initials1'),
            Committer('name2', 'email2', 'initials2')
        ]
        command = GetCommand(['get', 'committers'], Settings())
        command.execute()
        mock_print.assert_any_call('initials1 - name1 <email1>')
        mock_print.assert_any_call('initials2 - name2 <email2>')