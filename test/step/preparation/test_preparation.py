import unittest
from unittest.mock import Mock

from guet.steps.preparation.preapration import Preparation
from guet.steps.step import Step


class TestPreparation(unittest.TestCase):

    def test_do_play_calls_prepare(self):
        next_step: Step = Mock()

        prep = Preparation()
        prep.next(next_step)
        prep.prepare = Mock()

        prep.do_play([])

        prep.prepare.assert_called_once()
