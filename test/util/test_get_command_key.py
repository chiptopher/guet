from unittest import TestCase
from guet.util import get_command_key


class TestGetCommandKey(TestCase):
    def test_returns_first_argument_in_list(self):
        single_args = ['first']
        multiple_args = ['first', 'second']

        self.assertEqual('first', get_command_key(single_args))
        self.assertEqual('first', get_command_key(multiple_args))

    def test_returns_help_if_no_args_given(self):
        self.assertEqual('help', get_command_key([]))
