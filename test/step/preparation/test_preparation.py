import unittest
from unittest.mock import patch, call, Mock
from guet.steps.step import Step
from guet.steps.preparation.preapration import Preparation


class TestPreparation(unittest.TestCase):

    def test_do_play_calls_prepare(self):
        next_step: Step = Mock()

        prep = Preparation()
        prep.next(next_step)
        prep.prepare = Mock()

        prep.do_play()

        prep.prepare.assert_called_once()
