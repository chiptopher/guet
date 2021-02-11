import unittest
from unittest.mock import Mock, call, patch

from guet.steps.check.check import Check
from guet.steps.step import Step


class TestCheck(unittest.TestCase):
    def test_do_play_calls_next_play_if_should_stop_returns_false(self):
        next_step: Step = Mock()

        check = Check("stop")
        check.next(next_step)
        check.should_stop = lambda args: False

        check.play([])

        next_step.play.assert_called_once()

    @patch('builtins.exit')
    @patch('builtins.print')
    def test_do_play_calls_exit_if_should_stop_is_true(self, mock_print, mock_exit):
        next_step: Step = Mock()

        check = Check("stop")
        check.next(next_step)
        check.should_stop = lambda args: True

        check.do_play([])

        mock_exit.assert_called_with(1)

    @patch('builtins.exit')
    @patch('builtins.print')
    def test_play_prints_error_message_when_not_calling_next_play(self, mock_print, mock_exit):
        next_step: Step = Mock()

        stop_message = "stop"
        check = Check(stop_message)
        check.next(next_step)
        check.should_stop = lambda args: True

        check.do_play([])

        mock_print.assert_called_with(stop_message)

    @patch('builtins.exit')
    @patch('builtins.print')
    def test_calls_subclass_message_hook_if_one_not_prodivded_by_constructor(self, mock_print, mock_exit):
        next_step: Step = Mock()

        stop_message = "stop"
        check = Check()
        check.next(next_step)
        check.should_stop = lambda args: True
        check.load_message = lambda args: stop_message

        check.do_play([])

        mock_print.assert_called_with(stop_message)
