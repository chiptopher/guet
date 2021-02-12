from pathlib import Path
from unittest import TestCase
from unittest.mock import Mock, patch

from guet.files import FileSystem


class TestFileSystem(TestCase):

    @patch('guet.files._file_system.File')
    def test_get_returns_file_with_at_path(self, mock_file):
        path = Path('/path/to/file')

        file_system = FileSystem()
        get = file_system.get(path)
        self.assertEqual(mock_file.return_value, get)

    @patch('guet.files._file_system.File', side_effect=[Mock(), Mock()])
    def test_get_returns_same_reference_when_requesting_file_more_than_once(self, mock_file):
        path = Path('/path/to/file')

        file_system = FileSystem()
        file1 = file_system.get(path)
        file2 = file_system.get(path)

        self.assertTrue(file1 == file2)

    @patch('guet.files._file_system.File', side_effect=[Mock(), Mock()])
    def test_save_all_calls_save_on_all_files(self, mock_file):
        file1 = Mock()
        file2 = Mock()
        mock_file.side_effect = [file1, file2]
        file_system = FileSystem()
        file_system.get(Path('/path/to/file1'))
        file_system.get(Path('/path/to/file2'))

        file_system.save_all()

        file1.save.assert_called()
        file2.save.assert_called()
