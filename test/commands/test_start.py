
from test.commands.test_command import CommandTest, create_test_case
from guet.commands.start import StartCommand
from guet.gateway import *
from unittest.mock import Mock


class TestStartCommand(CommandTest):

    def test_validate(self):
        cases = [
            create_test_case(['start'], True, 'Should return true with the correct number of args'),
            create_test_case(['nother'], False, 'Should return false if the correct number of args is arent correct'),
            create_test_case([], False, 'Should return false when there are less than the number of args')
        ]

        for case in cases:
            self._validate_test(case, StartCommand)

    def test_execute_adds_the_hook(self):
        mock_git_gateway = GitGateway()
        mock_git_gateway.add_commit_msg_hook = Mock()
        mock_git_gateway.git_present = Mock(return_value=True)

        command = StartCommand([], mock_git_gateway)
        command.execute()

        mock_git_gateway.add_commit_msg_hook.assert_called_once()

    def test_get_short_help_message(self):
        self.assertEqual('Start guet usage in the repository at current directory', StartCommand.get_short_help_message())
