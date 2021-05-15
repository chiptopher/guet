from unittest import TestCase
from unittest.mock import Mock

from guet.committers.committer import Committer
from guet.hooks._commit_msg import CommitMsg


class TestCommitMsg(TestCase):
    def test_execute_sets_commit_message_to_current_committers(self):
        current_committers = Mock()
        current_committers.get = Mock(return_value=[
            Committer('name1', 'email1', 'initials1'),
            Committer('name2', 'email2', 'initials2'),
        ])

        git = Mock()

        git.commit_msg = ['initial commit']

        action = CommitMsg(current_committers, git)
        action.execute([])

        self.assertEqual(git.commit_msg, [
            'initial commit',
            '',
            'Co-authored-by: name1 <email1>',
            'Co-authored-by: name2 <email2>',
        ])
