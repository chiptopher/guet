from unittest import TestCase
from unittest.mock import Mock

from guet.committers.committer import Committer

from guet.commands.scriptcommands.postcommit.postcommit_strategy import PostCommitStrategy
from guet.context.context import Context


class TestPostCommitStrategy(TestCase):

    def test_rotates_first_current_committer_to_last_committer(self):
        context: Context = Mock()
        context.committers = Mock()
        context.committers.current.return_value = [
            Committer('name1', 'email1', 'initials1'),
            Committer('name2', 'email2', 'initials2')
        ]

        strategy = PostCommitStrategy(context)
        strategy.apply()

        context.set_committers.assert_called_with([
            Committer('name2', 'email2', 'initials2'),
            Committer('name1', 'email1', 'initials1')
        ])
