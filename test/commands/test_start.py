from unittest.mock import Mock, patch, call

from guet.commands.start import StartCommand
from guet.git.git_gateway import GitGateway
from test.commands.test_command import CommandTest, create_test_case
from guet.gateways.io import PrintGateway, InputGateway
from guet.git.create_hook import HookMode, Hooks


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

    @patch('guet.commands.start.create_hook')
    @patch("guet.commands.start.git_hook_path_from_cwd")
    @patch("guet.commands.start.any_hooks_present")
    def test_execute_adds_the_hook(self, mock_any_hooks_present, git_hook_path_from_cwd, mock_create_hook):
        git_hook_path_from_cwd.return_value = '/path'
        mock_any_hooks_present.return_value = False

        mock_git_gateway = GitGateway()
        mock_git_gateway.add_hooks = Mock()
        mock_git_gateway.git_present = Mock(return_value=True)

        command = StartCommand([], mock_git_gateway)
        command.execute()
        mock_any_hooks_present.assert_called_once_with('/path')
        mock_create_hook.assert_has_calls([
            call('/path', Hooks.PRE_COMMIT, HookMode.NEW_OR_OVERWRITE),
            call('/path', Hooks.POST_COMMIT, HookMode.NEW_OR_OVERWRITE),
            call('/path', Hooks.COMMIT_MSG, HookMode.NEW_OR_OVERWRITE)
        ])

    @patch('guet.commands.start.create_hook')
    @patch("guet.commands.start.git_hook_path_from_cwd")
    @patch("guet.commands.start.any_hooks_present")
    def test_execute_prompts_user_for_input_when_hooks_already_exist(self,
                                                                     mock_any_hooks_presnet,
                                                                     git_hook_path_from_cwd,
                                                                     mock_create_hook):
        mock_any_hooks_presnet.return_value = True
        git_hook_path_from_cwd.return_value = 'path'

        self.mock_input_gateway.input = Mock(return_value='c')

        command = self._create_command([])
        command.execute()

        self.mock_print_gateway.print.assert_called_once_with(
            'There is already commit hooks in this project. Would you like to overwrite (o), create (c) the file and put it in the hooks folder, or cancel (x)?')
        self.mock_input_gateway.input.assert_called_once()

    @patch('guet.commands.start.create_hook')
    @patch("guet.commands.start.git_hook_path_from_cwd")
    @patch("guet.commands.start.any_hooks_present")
    def test_execute_wont_create_hooks_if_user_chooses_to_cancel(self,
                                                                 mock_any_hooks_presenet,
                                                                 git_hook_path_from_cwd,
                                                                 mock_create_hook):
        mock_any_hooks_presenet.return_value = True
        git_hook_path_from_cwd.return_value = 'path'

        self.mock_input_gateway.input = Mock(return_value='x')

        command = self._create_command([])
        command.execute()
        mock_create_hook.assert_not_called()

    @patch('guet.commands.start.create_hook')
    @patch("guet.commands.start.git_hook_path_from_cwd")
    @patch("guet.commands.start.any_hooks_present")
    def test_execute_will_overwrite_if_input_is_o(self, mock_any_hooks_present, git_hook_path_from_cwd, mock_create_hook):

        mock_any_hooks_present.return_value = True
        git_hook_path_from_cwd.return_value = 'path'

        self.mock_input_gateway.input = Mock(return_value='o')

        command = self._create_command([])
        command.execute()
        mock_create_hook.assert_has_calls([
            call('path', Hooks.PRE_COMMIT, HookMode.NEW_OR_OVERWRITE),
            call('path', Hooks.POST_COMMIT, HookMode.NEW_OR_OVERWRITE),
            call('path', Hooks.COMMIT_MSG, HookMode.NEW_OR_OVERWRITE)
        ])

    def test_get_short_help_message(self):
        self.assertEqual('Start guet usage in the repository at current directory',
                         StartCommand.get_short_help_message())

    def _create_command(self, args: list, git_gateway: GitGateway = None, print_gateway: PrintGateway = None,
                        input_gateway: InputGateway = None):
        gg = git_gateway if None else self.mock_git_gateway
        pg = print_gateway if None else self.mock_print_gateway
        ig = input_gateway if None else self.mock_input_gateway
        return StartCommand(args, gg, pg, ig)
