import unittest
from unittest.mock import Mock, call, patch

from guet.commands.addcommitter.factory import AddCommitterFactory, ADD_COMMITTER_HELP_MESSAGE
from guet.settings.settings import Settings


@patch('guet.commands.addcommitter.add_committer_strategy.add_committer')
@patch('builtins.print')
class TestAddUserCommand(unittest.TestCase):
    def test_execute_prints_error_message_when_too_many_arguments_are_given(
            self, mock_print, mock_add_commiter):
        initials = 'usr'
        name = 'user'
        email = 'user@localhost'

        command = AddCommitterFactory().build(['add', initials, name, email, 'extra'], Settings())
        command.execute()

        mock_print.assert_called_once_with('Too many arguments.')

    def test_execute_prints_the_error_message_and_help_message_when_there_are_not_enough_args(
            self, mock_print, mock_add_commiter):
        command = AddCommitterFactory().build(['guet', 'initials', 'name'], Settings())
        command.execute()

        calls = [
            call('Not enough arguments.'),
            call(''),
            call(ADD_COMMITTER_HELP_MESSAGE)
        ]
        mock_print.assert_has_calls(calls)

    def test_get_short_help_message(self, mock_print, mock_add_commiter):
        self.assertEqual('Add committer to the list of available committers',
                         AddCommitterFactory().short_help_message())

    def test_execute_also_adds_committer_to_committers_file(self, mock_print, mock_add_commiter):
        command = AddCommitterFactory().build(['add', 'initials', 'name', 'email'], Settings())
        command.execute()

        mock_add_commiter.assert_called_with('initials', 'name', 'email')
