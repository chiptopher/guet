import unittest
from unittest.mock import patch

from guet.settings.settings import Settings


class TestSettings(unittest.TestCase):

    def test_load_parses_lines_and_builds_configuration_object(self):
        config = Settings()
        config.load([
            '2.0.0\n',
            '\n',
            'pairReset=true\n'
        ])
        self.assertEqual(True, config.read('pairReset'))

    def test_load_can_parse_a_config_file_that_only_had_the_version_number(self):
        config = Settings()
        config.load([
            '2.0.0\n',
            '\n'
        ])
        self.assertEqual(False, config.read('debug'))

    @patch('builtins.print')
    @patch('builtins.exit')
    def test_load_prints_message_about_bad_configuration_when_file_has_invalid_configuration_option(self,
                                                                                                    mock_exit,
                                                                                                    mock_print):
        config = Settings()
        config.load([
            '2.0.0\n',
            '\n',
            'unknownKey=true\n'
        ])
        mock_print.assert_called_with('Unknown configuration value \"unknownKey\" in configuration file.')

    @patch('builtins.print')
    @patch('builtins.exit')
    def test_load_exits_when_given_invalid_key(self,
                                               mock_exit,
                                               mock_print):
        config = Settings()
        config.load([
            '2.0.0\n',
            '\n',
            'unknownKey=true\n'
        ])
        mock_exit.assert_called_with(1)

    def test_load_writes_the_version_number(self):
        config = Settings()
        config.load([
            '2.0.0\n',
            '\n',
            'pairReset=true\n'
        ])
        self.assertEqual('2.0.0', config.version)

    def test_write_returns_configuration_as_lines(self):
        config = Settings()
        config.load([
            '2.0.0\n',
            '\n',
            'pairReset=False\n'
        ])
        result = config.write()
        self.assertEqual([
            '2.0.0\n',
            '\n',
            'pairReset=False\n'
        ], result)

    def test_write_includes_version_number(self):
        config = Settings()
        config.load([
            '2.0.0\n',
            '\n',
            'pairReset=False\n'
        ])
        result = config.write()
        self.assertEqual([
            '2.0.0\n',
            '\n',
            'pairReset=False\n'
        ], result)

    def test_write_ignores_attributes_that_are_set_to_their_default_values(self):
        config = Settings()
        config.load([
            '2.0.0\n',
            '\n',
            'pairReset=True\n'
        ])
        result = config.write()
        self.assertEqual([
            '2.0.0\n',
            '\n'
        ], result)
