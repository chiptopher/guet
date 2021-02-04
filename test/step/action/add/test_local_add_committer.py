from pathlib import Path
import unittest
from unittest.mock import Mock, patch

from guet.committers.committers import Committers
from guet.steps.action.add.local_add_committer import LocalAddCommitter
from guet.committers.local_committer import LocalCommitter


@patch('guet.commands.add._local_add.project_root')
class TestLocalAddCommitter(unittest.TestCase):

    def test_execute_adds_local_committer_to_committers(self, mock_project_root):
        root = Path('/path/to/project/root')
        committers: Committers = Mock()
        action = LocalAddCommitter(committers, root)

        action.execute(['initials', 'name', 'email'])

        expected = LocalCommitter(
            initials='initials', name='name', email='emai', project_root=root)

        committers.add.assert_called_with(expected)
