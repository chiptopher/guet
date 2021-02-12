from unittest import TestCase

from guet.commands.add._args import ArgumentCheck


class TestArgumentCheck(TestCase):

    def test_should_stops_when_not_enough_args(self):
        check = ArgumentCheck()
        self.assertTrue(check.should_stop(['np', 'Name Person']))

    def test_load_messages_tells_user_when_they_dont_have_enough_args(self):
        args = ['np', 'Name Person']
        check = ArgumentCheck()
        self.assertEqual('Not enough arguments.', check.load_message(args))

    def test_should_stopl_when_too_many_args(self):
        args = ['np', 'Name Person', 'np@example.com', 'extra']
        check = ArgumentCheck()
        self.assertTrue(check.should_stop(args))

    def test_load_messages_tells_user_when_they_dont_have_too_many_args(self):
        args = ['np', 'Name Person', 'np@example.com', 'extra']
        check = ArgumentCheck()
        self.assertEqual('Too many arguments.', check.load_message(args))

    def test_should_not_stop_if_correct_arg_count_and_local_flag_given(self):
        args = ['np', 'Name Person', 'np@example.com', '--local']
        check = ArgumentCheck()
        self.assertFalse(check.should_stop(args))
