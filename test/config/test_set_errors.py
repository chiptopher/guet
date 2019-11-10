import unittest
from os.path import join
from unittest.mock import patch

from guet import constants
from guet.config import configuration_directory
from guet.config.set_errors import set_errors


@patch('guet.config.set_errors.write_lines')
class TestSetErrors(unittest.TestCase):
    def test_writes_lines_to_errors_file(self,
                                         mock_write_lines):
        lines = [
            'line1\n',
            'line2\n'
        ]
        set_errors(lines)
        mock_write_lines.assert_called_with(join(configuration_directory, constants.ERRORS), lines)
