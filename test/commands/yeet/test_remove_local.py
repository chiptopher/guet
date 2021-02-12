from pathlib import Path
from unittest import TestCase
from unittest.mock import patch

from guet.commands.yeet._remove_local import RemoveLocal


@patch('builtins.print')
@patch('guet.commands.yeet._remove_local.isdir', return_value=True)
@patch('guet.commands.yeet._remove_local.project_root', return_value=Path('path/to/root'))
@patch('guet.commands.yeet._remove_local.rmtree')
class TestRemoveLocal(TestCase):
    def test_removes_local_guet_directory(self, mockrmtree, mock_root, _1, _2,):
        remove_local = RemoveLocal()
        remove_local.execute([])

        mockrmtree.assert_called_with(mock_root.return_value.joinpath('.guet'))

    def test_prints_error_message_when_no_guet_present(self, mockrmtree, _, mock_isdir, mock_print):
        mock_isdir.return_value = False
        remove_local = RemoveLocal()
        remove_local.execute([])

        mockrmtree.assert_not_called()
        mock_print.assert_called_with('No local guet configurations for this project')
