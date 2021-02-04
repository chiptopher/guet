from unittest import TestCase
from unittest.mock import Mock

from guet.commands.add._local_add import AddCommittersLocally
from guet.committers import GlobalCommitter


class TestAddCommittersLocally(TestCase):
    def test_execute_adds_local_committer(self):
        committers = Mock()
        command = AddCommittersLocally(committers)
        command.execute(['initials', 'name', 'email'])

        committers.add.assert_called_with(GlobalCommitter('name', 'email', 'initials'))
