from unittest import TestCase
from unittest.mock import Mock, patch

from guet.committers.committer import Committer
from guet.hooks._commit_msg import CommitMsg


class TestCommitMsg(TestCase):
    def test_execute_sets_commit_message_to_current_committers(self):
        committers = Mock()
        committers.current = Mock(return_value=[
            Committer('name1', 'email1', 'initials1'),
            Committer('name2', 'email2', 'initials2'),
        ])

        git = Mock()

        action = CommitMsg(committers, git)
        action.execute([])

        self.assertEqual(git.commit_msg, [
            'Co-authored-by: name1 <email1>',
            'Co-authored-by: name2 <email2>',
        ])

