import unittest
from unittest.mock import patch
from guet.steps.check.help_check import HelpCheck


class TestHelpCheck(unittest.TestCase):

    @patch('builtins.print')
    def test_should_stop_returns_true_if_help_flag_in_arguments(self, mock_print):
        help_message = "help message"
        check = HelpCheck(help_message)
        self.assertTrue(check.should_stop(['--help']))
        self.assertTrue(check.should_stop(['-h']))
        self.assertFalse(check.should_stop(['anything else']))

    @patch('builtins.print')
    def test_should_stop_returns_true_if_no_args_given_when_stop_on_no_args_is_true(self, mock_print):
        help_message = "help message"
        check = HelpCheck(help_message, stop_on_no_args=True)
        self.assertTrue(check.should_stop([]))
