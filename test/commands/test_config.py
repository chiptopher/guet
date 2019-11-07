import unittest
from unittest.mock import patch

from guet.commands.config import ConfigSetCommand
from guet.settings.settings import Settings


class ConfigSetTest(unittest.TestCase):

    def test_help_message(self):
        command = ConfigSetCommand([])
        self.assertEqual(ConfigSetCommand.HELP_MESSAGE, command.help())

    def test_short_help_message(self):
        command = ConfigSetCommand([])
        self.assertEqual(ConfigSetCommand.SHORT_HELP_MESSAGE, command.get_short_help_message())

    @patch('guet.commands.config.set_config')
    @patch('guet.commands.config.get_config')
    def test_execute_writes_the_new_config(self,
                                           mock_get_config,
                                           mock_set_config):
        mock_settings = Settings()
        mock_get_config.return_value = mock_settings
        command = ConfigSetCommand(['config', '--debug=True'])
        command.execute()
        mock_set_config.assert_called_with(mock_settings)
        self.assertEqual(True, mock_settings.read('debug'))

    @patch('guet.commands.config.set_config')
    @patch('guet.commands.config.get_config')
    def test_execute_writes_the_new_config_with_multiple_configs(self,
                                                                 mock_get_config,
                                                                 mock_set_config):
        mock_settings = Settings()
        mock_get_config.return_value = mock_settings
        command = ConfigSetCommand(['config', '--debug=True', '--pairReset=False'])
        command.execute()
        mock_set_config.assert_called_with(mock_settings)
        self.assertEqual(True, mock_settings.read('debug'))
        self.assertEqual(False, mock_settings.read('pairReset'))

    @patch('guet.commands.config.set_config')
    @patch('guet.commands.config.get_config')
    def test_execute_writes_the_new_config(self,
                                           mock_get_config,
                                           mock_set_config):
        mock_settings = Settings()
        mock_get_config.return_value = mock_settings
        command = ConfigSetCommand(['config', '--debug=True', 'noDoubleDash=True'])
        command.execute()
        mock_set_config.assert_called_with(mock_settings)
        self.assertEqual(True, mock_settings.read('debug'))

    @patch('builtins.exit')
    @patch('builtins.print')
    @patch('guet.commands.config.set_config')
    @patch('guet.commands.config.get_config')
    def test_execute_prints_error_message_when_given_bad_key(self,
                                                             mock_get_config,
                                                             mock_set_config,
                                                             mock_print,
                                                             mock_exit):
        mock_settings = Settings()
        mock_get_config.return_value = mock_settings
        command = ConfigSetCommand(['config', '--invalidKey=true'])
        command.execute()
        mock_print.assert_called_with(f'Cannot set \"invalidKey\", not valid configuration.\n')
        mock_exit.assert_called_with(1)
