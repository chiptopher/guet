import unittest
from pathlib import Path
from unittest.mock import Mock
from guet.committers.committers import Committers
from guet.steps.action.add.local_add_committer import LocalAddCommitter
from guet.committers.local_committer import LocalCommitter


class TestLocalAddCommitter(unittest.TestCase):

    def test_execute_adds_local_committer_to_committers(self):
        root = Path('/path/to/project/root')
        committers: Committers = Mock()
        action = LocalAddCommitter(committers, root)

        action.execute(['initials', 'name', 'email'])

        expected = LocalCommitter(
            initials='initials', name='name', email='emai', project_root=root)

        committers.add.assert_called_with(expected)
