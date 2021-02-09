from unittest import TestCase
from unittest.mock import Mock

from guet.steps import IfStep


class TestIfStep(TestCase):
    def test_plays_given_steps_if_condition_returns_true(self):
        steps = Mock()
        if_step = IfStep(lambda _: True, steps)

        args = []

        if_step.do_play(args)
        steps.play.assert_called_with(args)
