import unittest
from unittest.mock import Mock, call, patch

from guet.commands.addcommitter import AddUserCommand
from guet.settings.settings import Settings


@patch('guet.commands.addcommitter.already_initialized')
@patch('guet.commands.addcommitter.add_committer')
@patch('builtins.print')
class TestAddUserCommand(unittest.TestCase):


    def test_execute_prints_error_message_when_too_many_arguments_are_given(self,
                                                                            mock_print,
                                                                            mock_add_commiter,
                                                                            mock_already_initialized):
        initials = 'usr'
        name = 'user'
        email = 'user@localhost'
        command = AddUserCommand(['guet', initials, name, email, 'extra'], Settings())
        command.execute()

        mock_print.assert_called_once_with('Too many arguments.')

    def test_execute_prints_the_error_message_and_help_message_when_there_are_not_enough_args(self,
                                                                                              mock_print,
                                                                                              mock_add_commiter,
                                                                                              mock_already_initialized):
        command = AddUserCommand(['guet', 'initials', 'name'], Settings())
        command.execute()

        calls = [call('Not enough arguments.'), call(''), call(command.help())]
        mock_print.assert_has_calls(calls)

    def test_help_prints_the_help_message(self,
                                          mock_print,
                                          mock_add_commiter,
                                          mock_already_initialized):
        command = AddUserCommand([], Settings())
        self.assertEqual('usage: guet add <initials> <"name"> <email>', command.help())

    def test_get_short_help_message(self,
                                    mock_print,
                                    mock_add_commiter,
                                    mock_already_initialized):
        self.assertEqual('Add committer to the list of available committers', AddUserCommand.get_short_help_message())

    def test_execute_prints_error_message_when_init_hasnt_been_ran(self,
                                                                   mock_print,
                                                                   mock_add_commiter,
                                                                   mock_already_initialized):
        initials = 'usr'
        name = 'user'
        email = 'user@localhost'
        command = AddUserCommand(['guet', initials, name, email], Settings())
        mock_already_initialized.return_value = False
        command.execute()

        mock_print.assert_called_once_with(
            'guet has not been initialized yet! Please do so by running the command "guet init".')

    def test_execute_also_adds_committer_to_committers_file(self,
                                                            mock_print,
                                                            mock_add_commiter,
                                                            mock_already_initialized):
        command = AddUserCommand(['guet', 'initials', 'name', 'email'], Settings())
        command.execute()

        mock_add_commiter.assert_called_with('initials', 'name', 'email')
