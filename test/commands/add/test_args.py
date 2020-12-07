from unittest import TestCase

from guet.commands.add._args import ArgumentCheck


class TestArgumentCheck(TestCase):

    def test_should_stops_when_not_enough_args(self):
        check = ArgumentCheck()
        self.assertTrue(check.should_stop(['np', 'Name Person']))

    def test_load_messages_tells_user_when_they_dont_have_enough_args(self):
        check = ArgumentCheck()
        self.assertEqual('Not enough arguments.',
                         check.load_message(['np', 'Name Person']))
