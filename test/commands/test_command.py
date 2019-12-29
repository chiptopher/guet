import collections
import unittest
from unittest.mock import patch

from guet.commands.argsettingcommand import *

test_case = collections.namedtuple('TestCase', 'input expected_output explanation')


class TestCommand2(unittest.TestCase):
    class CommandImpl(ArgSettingCommand):
        called = False

        @classmethod
        def help_short(cls):
            return 'Short Help'

        def execute_hook(self):
            self.called = True

        def help(self):
            return 'Help'

    def test_execute_calls_implementation_command_hook(self):
        command = self.CommandImpl(['command2', 'arg'], Settings())
        command.execute()
        self.assertTrue(command.called)

    @patch('builtins.print')
    def test_prints_help_message_when_no_args_given_with_appended_newline(self,
                                                                          mock_print):
        command = self.CommandImpl(['command2'], Settings())
        command.execute()
        mock_print.assert_called_with('Help\n')

    def test_short_message_works(self):
        command = self.CommandImpl(['command2'], Settings())
        self.assertEqual('Short Help', command.get_short_help_message())

    @patch('builtins.print')
    def test_does_not_print_help_message_when_no_args_given_if_that_is_valid_for_command(self,
                                                                                         mock_print):
        command = self.CommandImpl(['command2'], Settings(), args_needed=False)
        mock_print.assert_not_called()
