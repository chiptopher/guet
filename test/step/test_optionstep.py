from unittest import TestCase
from unittest.mock import Mock

from guet.errors import UnexpectedError
from guet.steps import OptionStep


class TestOptionStep(TestCase):

    def test_returns_step_that_matches_option(self):
        choice = Mock()
        choice.return_value = 0

        first = Mock()

        choices = [first]

        step = OptionStep(choices, choice)

        self.assertEqual(first, step.do_play([]))

    def test_raises_exception_if_arg_not_in_list(self):
        choice = Mock()
        choice.return_value = 1

        first = Mock()

        choices = [first]

        step = OptionStep(choices, choice)

        self.assertRaises(UnexpectedError, step.do_play, [])
