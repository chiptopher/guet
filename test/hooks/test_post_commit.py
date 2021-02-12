from unittest import TestCase
from unittest.mock import Mock

from guet.committers.committer import Committer
from guet.hooks._post_commit import PostCommit


class TestPostCommit(TestCase):
    def test_roates_first_committer_to_last(self):
        current_committers = Mock()

        first = Committer('name1', 'email1', 'initials1')
        second = Committer('name2', 'email2', 'initials2')

        current_committers.get.return_value = [first, second]

        hook = PostCommit(current_committers)
        hook.play([])

        current_committers.set.assert_called_with([second, first])

    def test_handles_only_one_committer(self):
        current_committers = Mock()

        first = Committer('name1', 'email1', 'initials1')

        current_committers.get.return_value = [first]

        hook = PostCommit(current_committers)
        hook.play([])

        current_committers.set.assert_not_called()
