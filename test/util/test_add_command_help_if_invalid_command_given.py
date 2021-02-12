from unittest import TestCase

from guet.util import add_command_help_if_invalid_command_given


class TestAddCommandHelpIfInvalidCommandGiven(TestCase):
    def test_adds_help_if_flag_given_without_command(self):
        args = ['--version']
        result = add_command_help_if_invalid_command_given(args)
        self.assertEqual(['help', '--version'], result)

    def test_adds_help_if_no_args_given(self):
        args = []
        result = add_command_help_if_invalid_command_given(args)
        self.assertEqual(['help'], result)
