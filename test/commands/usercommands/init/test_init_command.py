from unittest import TestCase
from unittest.mock import patch, Mock

from guet.commands.usercommands.init._init_command import InitCommand
from guet.config.errors import AlreadyInitializedError


class TestInitCommand(TestCase):

    @patch('builtins.print')
    def test_prints_error_message_when_catching_already_initialized_error(self, mock_print):
        mock_context = Mock()
        mock_context.initialize = Mock(side_effect=AlreadyInitializedError)
        command = InitCommand(mock_context)
        command.execute()

        mock_print.assert_called_with('Config folder already exists.')
