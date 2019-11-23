import unittest
from os.path import join
from unittest.mock import patch

from guet import constants
from guet.config import CONFIGURATION_DIRECTORY
from guet.config.set_config import set_config
from guet.settings.settings import Settings


@patch('guet.config.set_config.write_lines')
class TestSetConfig(unittest.TestCase):

    def test_converts_settings_to_lines_and_writes_to_config_file(self,
                                                                  mock_write_lines):
        settings = Settings()
        settings.load([
            '2.0.0\n',
            '\n',
            'pairReset=False\n'
        ])
        set_config(settings)
        expected_result = [
            '2.0.0\n',
            '\n',
            'pairReset=False\n'
        ]
        mock_write_lines.assert_called_with(join(CONFIGURATION_DIRECTORY, constants.CONFIG), expected_result)
