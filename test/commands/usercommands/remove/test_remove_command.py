from unittest import TestCase
from unittest.mock import Mock, patch

from guet.commands.usercommands.remove import RemoveCommand
from guet.committers.committers import Committers
from guet.context.context import Context
from guet.errors import InvalidInitialsError


class TestRemoveCommand(TestCase):
    def test_removes_user(self):
        mock_context: Context = Mock()
        mock_committers: Committers = Mock()
        mock_context.committers = mock_committers

        command = RemoveCommand(mock_context, 'initials')
        command.execute()

        mock_committers.remove.assert_called_with(mock_committers.by_initials.return_value)

    @patch('builtins.print')
    def test_prints_error_message_when_no_committer_exists_with_initials(self, mock_print):
        mock_context: Context = Mock()
        mock_committers: Committers = Mock()
        mock_committers.by_initials.side_effect = InvalidInitialsError()
        mock_context.committers = mock_committers

        command = RemoveCommand(mock_context, 'initials')
        command.execute()

        mock_print.assert_called_with('No committer exists with initials "initials"')

    def test_lowers_initials_before_using(self):
        mock_context: Context = Mock()
        mock_committers: Committers = Mock()
        mock_context.committers = mock_committers

        command = RemoveCommand(mock_context, 'INITIALS')
        command.execute()

        mock_committers.by_initials.assert_called_with('initials')
