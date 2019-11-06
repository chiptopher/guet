import unittest
from unittest.mock import patch

from guet.settings.settings import Settings


class TestSettings(unittest.TestCase):

    def test_load_parses_lines_and_builds_configuration_object(self):
        config = Settings()
        config.load([
            'pairReset=true'
        ])
        self.assertEqual(True, config.read('pairReset'))

    @patch('builtins.print')
    @patch('builtins.exit')
    def test_load_prints_message_about_bad_configuration_when_file_has_invalid_configuration_option(self,
                                                                                                    mock_exit,
                                                                                                    mock_print):
        config = Settings()
        config.load([
            'unknownKey=true'
        ])
        mock_print.assert_called_with('Unknown configuration value \"unknownKey\" in configuration file.')

    @patch('builtins.print')
    @patch('builtins.exit')
    def test_load_exits_when_given_invalid_key(self,
                                               mock_exit,
                                               mock_print):
        config = Settings()
        config.load([
            'unknownKey=true'
        ])
        mock_exit.assert_called_with(1)

    def test_write_returns_configuration_as_lines(self):
        config = Settings()
        config.load([
            'pairReset=False'
        ])
        result = config.write()
        self.assertEqual(['pairReset=False\n'], result)

    def test_write_ignores_attributes_that_are_set_to_their_default_values(self):
        config = Settings()
        config.load([
            'pairReset=True'
        ])
        result = config.write()
        self.assertEqual([], result)
