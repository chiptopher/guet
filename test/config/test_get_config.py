import unittest
from unittest.mock import patch

from guet.config.get_config import get_config


@patch('guet.config.get_config.read_lines')
class TestGetConfig(unittest.TestCase):
    def test_loads_settings_from_config_file_lines(self, mock_read_lines):
        mock_read_lines.return_value = [
            '2.0.0\n',
            '\n',
            'pairReset=False\n'
        ]
        settings = get_config()
        self.assertEqual(False, settings.read('pairReset'))
