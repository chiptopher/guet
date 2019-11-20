import unittest
from unittest.mock import Mock, patch

from guet.commands.init import InitDataSourceCommand
from guet.settings.settings import Settings


class TestInitDataSourceCommand(unittest.TestCase):

    @patch('guet.commands.init.already_initialized')
    @patch('guet.commands.init.initialize')
    def test_execute_uses_gateway_to_create_data_source(self,
                                                        mock_initialize,
                                                        mock_already_initialized):
        mock_already_initialized.return_value = False
        command = InitDataSourceCommand(['init'], Settings())
        command.execute()
        mock_initialize.assert_called()

    @patch('builtins.print')
    @patch('guet.commands.init.already_initialized')
    def test_execute_prints_out_error_message_when_calling_init_when_it_has_already_been_called(self,
                                                                                                mock_already_initialized,
                                                                                                mock_print):
        mock_already_initialized.return_value = True

        command = InitDataSourceCommand(['init'], Settings())
        command.execute()

        mock_print.assert_called_once_with('Config folder already exists.')

    @patch('builtins.print')
    def test_execute_prints_help_command_when_there_are_incorrect_arguments(self,
                                                                            mock_print):

        path_exists_mock = Mock()
        path_exists_mock.return_value = False

        command = InitDataSourceCommand(['init', 'invalid arg'], Settings())
        command.execute()

        mock_print.assert_called_with('Invalid arguments.\n\n   {}'.format(command.help()))

    def test_get_short_help_message(self):
        self.assertEqual('Initialize guet for use', InitDataSourceCommand.get_short_help_message())
