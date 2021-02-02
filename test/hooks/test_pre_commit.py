from unittest import TestCase
from unittest.mock import Mock, patch

from guet.committers.committer import Committer
from guet.hooks._pre_commit import PreCommit


class TestPreCommit(TestCase):
    def test_execute_sets_commit_message_to_current_committers(self):
        pass

