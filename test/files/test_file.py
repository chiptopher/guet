#pylint: disable=protected-access

from pathlib import Path
from unittest import TestCase
from unittest.mock import patch

from guet.files import File


class TestFile(TestCase):
    @patch('guet.files._file.read_lines')
    def test_read_returns_content_of_file(self, mock_read_lines):
        path = Path('/absolute/path/to/file')
        expected = [
            'line1\n',
            'line2\n'
        ]
        mock_read_lines.return_value = expected
        file = File(path)
        self.assertListEqual(expected, file.read())

    @patch('guet.files._file.read_lines')
    def test_read_returns_empty_list_when_file_not_present(self, mock_read_lines):
        path = Path('/absolute/path/to/file')
        mock_read_lines.side_effect = FileNotFoundError()

        file = File(path)
        self.assertListEqual([], file.read())

    @patch('guet.files._file.write_lines')
    def test_save_writes_content_to_file(self, mock_write_lines):
        path = Path('/absolute/path/to/file')
        expected = [
            'line1\n',
            'line2'
        ]
        file = File(path)
        file.write(expected)
        file.save()
        mock_write_lines.assert_called_with(path, expected)

    def test_write_clears_mark_for_deletion(self):
        file = File(Path('/absolute/path/to/file'))
        file.delete()
        file.write(['lines'])
        self.assertFalse(file._marked_for_deletion)

    @patch('guet.files._file.write_lines')
    def test_save_does_nothing_if_file_has_not_changed(self, mock_write_lines):
        path = Path('/absolute/path/to/file')
        file = File(path)
        file.save()
        mock_write_lines.assert_not_called()

    @patch('guet.files._file.remove')
    @patch('guet.files._file.write_lines')
    def test_save_does_not_write_lines_if_file_marked_for_deletion(self, mock_write_lines, _1):
        path = Path('/absolute/path/to/file')
        file = File(path)
        file.write(['line'])
        file.delete()
        file.save()
        mock_write_lines.assert_not_called()

    @patch('guet.files._file.write_lines')
    def test_save_writes_empty_file_if_written_with_no_lines(self, mock_write_lines):
        path = Path('/absolute/path/to/file')
        file = File(path)
        file.write([])
        file.save()
        mock_write_lines.assert_called_with(path, [])

    @patch('guet.files._file.remove')
    def test_save_removes_file_if_makred_for_deletion(self, mock_remove):
        path = Path('/absolute/path/to/file')
        file = File(path)
        file.delete()
        file.save()
        mock_remove.assert_called()

    @patch('guet.files._file.write_lines')
    @patch('guet.files._file.read_lines')
    def test_save_doesnt_write_if_non_existant_file_is_only_read_from(self,
                                                                      mock_read_lines,
                                                                      mock_write_lines):
        path = Path('/absolute/path/to/file')
        mock_read_lines.side_effect = FileNotFoundError()

        file = File(path)
        file.read()
        file.save()

        mock_write_lines.assert_not_called()

    @patch('guet.files._file.read_lines')
    def test_overwrite_replaces_content_that_matches_pattern_with_given_line(self, mock_read_lines):
        path = Path('/abolute/path/to/file')
        mock_read_lines.return_value = [
            'key1=oldvalue1\n',
            'key2=value2\n'
        ]
        file = File(path)

        def overwrite_key1(line: str):
            return line.startswith('key1')

        file.overwrite(overwrite_key1, 'key1=new_value1\n')
        self.assertListEqual([
            'key1=new_value1\n',
            'key2=value2\n'
        ], file.read())

    def test_delete_marks_file_for_deletion(self):
        file = File(Path('/path/to/file'))
        file.delete()

        self.assertTrue(file._marked_for_deletion)
