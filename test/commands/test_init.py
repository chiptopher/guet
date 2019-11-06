"""
Copyright 2018 Christopher M. Boyer

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

    http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.
"""
import unittest
from unittest.mock import Mock, patch

from guet.commands.init import InitDataSourceCommand


class TestInitDataSourceCommand(unittest.TestCase):

    @patch('guet.commands.init.already_initialized')
    @patch('guet.commands.init.initialize')
    def test_execute_uses_gateway_to_create_data_source(self,
                                                        mock_initialize,
                                                        mock_already_initialized):
        mock_already_initialized.return_value = False
        command = InitDataSourceCommand(['init'])
        command.execute()
        mock_initialize.assert_called()

    @patch('builtins.print')
    @patch('guet.commands.init.already_initialized')
    def test_execute_prints_out_error_message_when_calling_init_when_it_has_already_been_called(self,
                                                                                                mock_already_initialized,
                                                                                                mock_print):
        mock_already_initialized.return_value = True

        command = InitDataSourceCommand(['init'])
        command.execute()

        mock_print.assert_called_once_with('Config folder already exists.')

    @patch('builtins.print')
    def test_execute_prints_help_command_when_there_are_incorrect_arguments(self,
                                                                            mock_print):

        path_exists_mock = Mock()
        path_exists_mock.return_value = False

        command = InitDataSourceCommand(['init', 'invalid arg'])
        command.execute()

        mock_print.assert_called_with('Invalid arguments.\n\n   {}'.format(command.help()))

    def test_get_short_help_message(self):
        self.assertEqual('Initialize guet for use', InitDataSourceCommand.get_short_help_message())
