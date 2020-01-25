import unittest
from unittest.mock import patch, mock_open

from guet.files.read_lines import read_lines


class TestReadLines(unittest.TestCase):

    @patch('builtins.open', new_callable=mock_open())
    def test_opens_file_in_read_mode(self, mock_open):
        read_lines('path/to/file')
        mock_open.assert_called_with('path/to/file', 'r')

    @patch('builtins.open', new_callable=mock_open())
    def test_returns_lines_from_file(self, mock_open):
        expected = [
            'Line1',
            'Line2'
        ]
        mock_open.return_value.readlines.return_value = expected
        result = read_lines('path/to/file')
        self.assertEqual(expected, result)

    @patch('builtins.open', new_callable=mock_open())
    def test_closes_file(self, mock_open):
        read_lines('path/to/file')
        mock_open.return_value.close.assert_called()

    @patch('builtins.open', new_callable=mock_open())
    def test_strips_newlines_from_the_end_of_lines(self, mock_open):
        expected = [
            'Line1\n',
            'Line2\n'
        ]
        mock_open.return_value.readlines.return_value = expected
        result = read_lines('path/to/file')
        self.assertEqual(['Line1', 'Line2'], result)
