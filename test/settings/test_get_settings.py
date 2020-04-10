import unittest
from unittest.mock import patch

from guet.settings.get_settings import get_settings


@patch('guet.settings.get_settings.read_lines')
class TestGetSettings(unittest.TestCase):
    def test_loads_settings_from_config_file_lines(self, mock_read_lines):
        mock_read_lines.return_value = [
            '2.0.0\n',
            '\n',
            'pairReset=False\n'
        ]
        settings = get_settings()
        self.assertEqual(False, settings.read('pairReset'))
