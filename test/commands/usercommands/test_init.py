import unittest
from unittest.mock import patch

from guet.commands.usercommands.init.factory import InitCommandFactory
from guet.settings.settings import Settings


@patch('guet.commands.command_factory.Context')
class TestInitDataSourceCommand(unittest.TestCase):

    @patch('guet.commands.usercommands.init.factory.already_initialized')
    @patch('guet.commands.usercommands.init.factory.initialize')
    def test_execute_uses_gateway_to_create_data_source(self,
                                                        mock_initialize,
                                                        mock_already_initialized, _1):
        mock_already_initialized.return_value = False
        command = InitCommandFactory().build(['init'], Settings())
        command.execute()
        mock_initialize.assert_called()

    @patch('builtins.print')
    @patch('guet.commands.usercommands.init.factory.already_initialized')
    def test_execute_prints_out_error_message_when_calling_init_when_it_has_already_been_called(self,
                                                                                                mock_already_initialized,
                                                                                                mock_print, _1):
        mock_already_initialized.return_value = True

        command = InitCommandFactory().build(['init'], Settings())
        command.execute()

        mock_print.assert_called_once_with('Config folder already exists.')

    def test_get_short_help_message(self, _1):
        self.assertEqual('Initialize guet for use', InitCommandFactory().short_help_message())
