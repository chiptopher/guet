import unittest
from unittest.mock import patch, mock_open

from guet.files.write_lines import write_lines


class TestWriteLines(unittest.TestCase):

    @patch('builtins.open', new_callable=mock_open())
    def test_opens_file_in_overwrite_mode(self, mock_open):
        write_lines('path/to/file', [])
        mock_open.assert_called_with('path/to/file', 'w')

    @patch('builtins.open', new_callable=mock_open())
    def test_writes_lines_to_file(self, mock_open):
        expected = [
            'Line1\n',
            'Line2\n'
        ]
        mock_open.return_value.readlines.return_value = expected
        write_lines('path/to/file', expected)
        mock_open.return_value.writelines.assert_called_with(expected)

    @patch('builtins.open', new_callable=mock_open())
    def test_closes_file(self, mock_open):
        write_lines('path/to/file', [])
        mock_open.return_value.close.assert_called()

    @patch('builtins.open', new_callable=mock_open())
    def test_appends_newline_to_files_if_one_is_not_present(self, mock_open):
        given = [
            'Line1',
            'Line2\n'
        ]
        expected = [
            'Line1\n',
            'Line2\n'
        ]
        mock_open.return_value.readlines.return_value = given
        write_lines('path/to/file', given)
        mock_open.return_value.writelines.assert_called_with(expected)
