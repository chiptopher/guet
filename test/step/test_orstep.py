import unittest
from unittest.mock import Mock
from guet.steps.orstep import OrStep
from guet.steps.step import Step


class TestOrStep(unittest.TestCase):
    def test_do_play_calls_next_on_whichever_callable_chooses(self):
        step1: Step = Mock()
        step2: Step = Mock()
        or_step = OrStep(step1, step2, lambda args: True)

        args = []

        or_step.do_play(args)

        step1.play.assert_called_with(args)
