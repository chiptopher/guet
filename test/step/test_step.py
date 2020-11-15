import unittest
from unittest.mock import Mock
from guet.steps.step import Step


class TestStep(unittest.TestCase):
    def test_next_sets_next_step(self):
        first = Step()
        second = Step()
        first.next(second)

        self.assertEqual(first._next, second)

    def test_next_returns_head_of_chain(self):
        first = Step()
        second = Step()
        chain = first.next(second)

        self.assertEqual(chain, first)

    def test_next_returns_head_of_chain_when_there_are_many_steps(self):
        first = Step()
        chain = first.next(Step()).next(Step()).next(Step())

        self.assertEqual(chain, first)

    def test_next_appends_next_step_to_end_of_chain(self):
        first = Step()
        second = Step()
        third = Step()
        first.next(second).next(third)

        self.assertEqual(third, second._next)

    def test_play_calls_next_play_if_present(self):
        first = Step()
        first.do_play = Mock()
        second = Mock()
        first.next(second)

        first.play([])
        second.play.assert_called_once()

    def test_play_doesnt_call_next_play_if_no_next_present(self):
        first = Step()
        first.do_play = Mock()
        first.play([])

    def test_play_calls_self_do_play(self):
        first = Step()
        first.do_play = Mock()

        first.play([])

        first.do_play.assert_called_once()

    def test_play_only_called_once_per_link(self):
        first = Step()
        first.do_play = Mock()
        second = Step()
        second.do_play = Mock()
        third = Step()
        third.do_play = Mock()
        first.next(second).next(third)

        first.play([])
        second.do_play.assert_called_once()
        third.do_play.assert_called_once()