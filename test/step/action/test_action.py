import unittest
from unittest.mock import Mock
from guet.steps.action.action import Action


class TestAction(unittest.TestCase):
    def test_play_calls_action(self):
        action = Action()
        action.execute = Mock()
        action.do_play([])

        action.execute.assert_called_once()
