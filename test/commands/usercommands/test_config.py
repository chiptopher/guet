import unittest
from unittest.mock import patch

from guet.settings.settings import Settings
from guet.commands.usercommands.config.factory import ConfigCommandFactory


@patch('guet.commands.command_factory.Context')
class ConfigSetTest(unittest.TestCase):

    @patch('guet.commands.usercommands.config.set_config_strategy.set_config')
    @patch('guet.commands.usercommands.config.set_config_strategy.get_config')
    def test_execute_writes_the_new_config(self, mock_get_config, mock_set_config, _1):
        mock_settings = Settings()
        mock_get_config.return_value = mock_settings
        command = ConfigCommandFactory().build(['config', '--debug=True'], Settings())
        command.execute()
        mock_set_config.assert_called_with(mock_settings)
        self.assertEqual(True, mock_settings.read('debug'))

    @patch('guet.commands.usercommands.config.set_config_strategy.set_config')
    @patch('guet.commands.usercommands.config.set_config_strategy.get_config')
    def test_execute_writes_the_new_config_with_multiple_configs(self, mock_get_config,
                                                                 mock_set_config, _1):
        mock_settings = Settings()
        mock_get_config.return_value = mock_settings
        command = ConfigCommandFactory().build(['config', '--debug=True', '--pairReset=False'], Settings())
        command.execute()
        mock_set_config.assert_called_with(mock_settings)
        self.assertEqual(True, mock_settings.read('debug'))
        self.assertEqual(False, mock_settings.read('pairReset'))

    @patch('guet.commands.usercommands.config.set_config_strategy.set_config')
    @patch('guet.commands.usercommands.config.set_config_strategy.get_config')
    def test_execute_writes_multiple_configs(self, mock_get_config, mock_set_config, _1):
        mock_settings = Settings()
        mock_get_config.return_value = mock_settings
        command = ConfigCommandFactory().build(['config', '--debug=True', 'noDoubleDash=True'], Settings())
        command.execute()
        mock_set_config.assert_called_with(mock_settings)
        self.assertEqual(True, mock_settings.read('debug'))

    @patch('builtins.exit')
    @patch('builtins.print')
    @patch('guet.commands.usercommands.config.set_config_strategy.set_config')
    @patch('guet.commands.usercommands.config.set_config_strategy.get_config')
    def test_execute_prints_error_message_when_given_bad_key(self, mock_get_config, mock_set_config,
                                                             mock_print, mock_exit, _1):
        mock_settings = Settings()
        mock_get_config.return_value = mock_settings
        command = ConfigCommandFactory().build(['config', '--invalidKey=true'], Settings())
        command.execute()
        mock_print.assert_called_with(f'Cannot set \"invalidKey\", not valid configuration.\n')
        mock_exit.assert_called_with(1)
