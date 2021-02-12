from unittest import TestCase
from unittest.mock import Mock

from guet.errors import InvalidInitialsError
from guet.steps.check._committers_exist import CommittersExistCheck


class TestCommittersExistCheck(TestCase):

    def test_returns_true_if_committer_does_not_exist(self):
        committers = Mock()
        committers.by_initials.return_value = None
        check = CommittersExistCheck(committers)

        self.assertTrue(check.should_stop(['missing']))

    def test_returns_false_if_committer_exists(self):
        committers = Mock()
        committers.by_initials.return_value = Mock()
        check = CommittersExistCheck(committers)

        self.assertFalse(check.should_stop(['initials']))

    def test_load_message_returns_error_with_missing_initials(self):
        committers = Mock()
        committers.by_initials.return_value = None
        check = CommittersExistCheck(committers)

        message = check.load_message(['first', 'second'])

        expected = ("No committer exists with initials 'first'\n"
                    "No committer exists with initials 'second'")

        self.assertEqual(expected, message)
