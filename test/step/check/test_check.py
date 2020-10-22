import unittest
from unittest.mock import patch, call, Mock
from guet.steps.check.check import Check
from guet.steps.step import Step


class TestCheck(unittest.TestCase):
    def test_do_play_calls_next_play_if_should_stop_returns_false(self):
        next_step: Step = Mock()

        check = Check("stop")
        check.next(next_step)
        check.should_stop = lambda: False

        check.do_play()

        next_step.play.assert_called_once()

    @patch('builtins.print')
    def test_play_does_not_call_next_play_if_should_stop_returns_true(self, mock_print):
        next_step: Step = Mock()

        check = Check("stop")
        check.next(next_step)
        check.should_stop = lambda: True

        check.do_play()

        next_step.play.assert_not_called()

    @patch('builtins.print')
    def test_play_prints_error_message_when_not_calling_next_play(self, mock_print):
        next_step: Step = Mock()

        stop_message = "stop"
        check = Check(stop_message)
        check.next(next_step)
        check.should_stop = lambda: True

        check.do_play()

        mock_print.assert_called_with(stop_message)
