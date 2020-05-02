import unittest
from pathlib import Path
from unittest.mock import patch, mock_open, Mock

from guet.files.write_lines import write_lines


class TestWriteLines(unittest.TestCase):

    def test_writes_lines_to_file(self):
        path: Path = Mock()
        write_lines(path, [
            'Line1\n',
            'Line2\n'
        ])
        path.write_text.assert_called_with('Line1\nLine2\n')

    def test_appends_newline_to_files_if_one_is_not_present(self):
        path: Path = Mock()
        given = [
            'Line1',
            'Line2\n'
        ]
        write_lines(path, given)
        path.write_text.assert_called_with('Line1\nLine2\n')
