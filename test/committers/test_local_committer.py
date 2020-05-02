from pathlib import Path
from unittest import TestCase
from unittest.mock import patch

from guet import constants
from guet.committers.local_committer import LocalCommitter


@patch('guet.committers.local_committer.add_committer')
class TestLocalCommitterSave(TestCase):

    def test_adds_committer_to_project_root(self, mock_add_committer):
        committer = LocalCommitter('name', 'email', 'initials', Path('/path/to/root'))
        committer.save()
        file_path = Path('/path/to/root/').joinpath('.guet').joinpath(constants.COMMITTERS)
        mock_add_committer.assert_called_with('initials', 'name', 'email', file_path=file_path)
