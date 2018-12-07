
from unittest.mock import Mock

from guet.commands.start import StartCommand
from guet.gateways.gateway import *
from test.commands.test_command import CommandTest, create_test_case
from guet.gateways.io import PrintGateway, InputGateway


class TestStartCommand(CommandTest):

    def setUp(self):
        self.mock_git_gateway = GitGateway()
        self.mock_git_gateway.add_hooks = Mock()
        self.mock_git_gateway.commit_msg_hook_exists = Mock()
        self.mock_git_gateway.git_present = Mock()
        self.mock_git_gateway.hook_present = Mock()
        self.mock_git_gateway.any_hook_present = Mock()

        self.mock_print_gateway = PrintGateway()
        self.mock_print_gateway.print = Mock()

        self.mock_input_gateway = InputGateway()
        self.mock_input_gateway.input = Mock()

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
        mock_git_gateway.add_hooks = Mock()
        mock_git_gateway.git_present = Mock(return_value=True)

        command = StartCommand([], mock_git_gateway)
        command.execute()

        mock_git_gateway.add_hooks.assert_called_once()

    def test_execute_prompts_user_for_input_when_hooks_already_exist(self):
        self.mock_git_gateway.git_present = Mock(return_value=True)
        self.mock_git_gateway.any_hook_present = Mock(return_value=True)
        self.mock_input_gateway.input = Mock(return_value='x')

        command = self._create_command([])
        command.execute()

        self.mock_print_gateway.print.assert_called_once_with('There is already commit hooks in this project. Would you like to overwrite (o), create (c) the file and put it in the hooks folder, or cancel (x)?')
        self.mock_input_gateway.input.assert_called_once()

    def test_get_short_help_message(self):
        self.assertEqual('Start guet usage in the repository at current directory', StartCommand.get_short_help_message())

    def _create_command(self, args: list, git_gateway: GitGateway = None, print_gateway: PrintGateway = None, input_gateway: InputGateway = None):
        gg = git_gateway if None else self.mock_git_gateway
        pg = print_gateway if None else self.mock_print_gateway
        ig = input_gateway if None else self.mock_input_gateway
        return StartCommand(args, gg, pg, ig)
