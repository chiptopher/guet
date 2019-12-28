import unittest
from unittest.mock import Mock, patch, call

from guet.commands.start.factory import StartCommandFactory
from guet.git.create_hook import HookMode, Hooks
from guet.settings.settings import Settings


class TestStartCommand(unittest.TestCase):

    @patch('guet.commands.start.start_strategy.git_present_in_cwd')
    @patch('guet.commands.start.start_strategy.create_hook')
    @patch("guet.commands.start.start_strategy.git_hook_path_from_cwd")
    @patch("guet.commands.start.start_strategy.any_hooks_present")
    def test_execute_adds_the_hook(self,
                                   mock_any_hooks_present,
                                   git_hook_path_from_cwd,
                                   mock_create_hook,
                                   git_present_in_cwd):
        git_hook_path_from_cwd.return_value = '/path'
        mock_any_hooks_present.return_value = False

        command = StartCommandFactory().build([], Settings())
        command.execute()
        mock_any_hooks_present.assert_called_once_with('/path')
        mock_create_hook.assert_has_calls([
            call('/path', Hooks.PRE_COMMIT, HookMode.NEW_OR_OVERWRITE),
            call('/path', Hooks.POST_COMMIT, HookMode.NEW_OR_OVERWRITE),
            call('/path', Hooks.COMMIT_MSG, HookMode.NEW_OR_OVERWRITE)
        ])

    @patch('builtins.input')
    @patch('builtins.print')
    @patch('guet.commands.start.start_strategy.git_present_in_cwd')
    @patch('guet.commands.start.start_strategy.create_hook')
    @patch("guet.commands.start.start_strategy.git_hook_path_from_cwd")
    @patch("guet.commands.start.start_strategy.any_hooks_present")
    def test_execute_prompts_user_for_input_when_hooks_already_exist(self,
                                                                     mock_any_hooks_presnet,
                                                                     git_hook_path_from_cwd,
                                                                     mock_create_hook,
                                                                     git_present_in_cwd,
                                                                     mock_print,
                                                                     mock_input):
        mock_any_hooks_presnet.return_value = True
        git_hook_path_from_cwd.return_value = 'path'

        mock_input.return_value = 'c'

        command = StartCommandFactory().build([], Settings())
        command.execute()

        mock_print.assert_called_once_with(
            'There is already commit hooks in this project. Would you like to overwrite (o), create (c) the file and put it in the hooks folder, or cancel (x)?')
        mock_input.assert_called_once()

    @patch('builtins.input')
    @patch('guet.commands.start.start_strategy.git_present_in_cwd')
    @patch('guet.commands.start.start_strategy.create_hook')
    @patch("guet.commands.start.start_strategy.git_hook_path_from_cwd")
    @patch("guet.commands.start.start_strategy.any_hooks_present")
    def test_execute_wont_create_hooks_if_user_chooses_to_cancel(self,
                                                                 mock_any_hooks_presenet,
                                                                 git_hook_path_from_cwd,
                                                                 mock_create_hook,
                                                                 git_present_in_cwd,
                                                                 mock_input):
        mock_input.return_value = 'x'
        mock_any_hooks_presenet.return_value = True
        git_hook_path_from_cwd.return_value = 'path'

        command = StartCommandFactory().build([], Settings())
        command.execute()
        mock_create_hook.assert_not_called()

    @patch('builtins.input')
    @patch('guet.commands.start.start_strategy.git_present_in_cwd')
    @patch('guet.commands.start.start_strategy.create_hook')
    @patch("guet.commands.start.start_strategy.git_hook_path_from_cwd")
    @patch("guet.commands.start.start_strategy.any_hooks_present")
    def test_execute_will_overwrite_if_input_is_o(self,
                                                  mock_any_hooks_present,
                                                  git_hook_path_from_cwd,
                                                  mock_create_hook,
                                                  git_present_in_cwd,
                                                  mock_input):
        mock_input.return_value = 'o'
        mock_any_hooks_present.return_value = True
        git_hook_path_from_cwd.return_value = 'path'

        command = StartCommandFactory().build([], Settings())
        command.execute()
        mock_create_hook.assert_has_calls([
            call('path', Hooks.PRE_COMMIT, HookMode.NEW_OR_OVERWRITE),
            call('path', Hooks.POST_COMMIT, HookMode.NEW_OR_OVERWRITE),
            call('path', Hooks.COMMIT_MSG, HookMode.NEW_OR_OVERWRITE)
        ])

    @patch('builtins.print')
    @patch('guet.commands.start.start_strategy.git_present_in_cwd')
    @patch('guet.commands.start.start_strategy.create_hook')
    @patch("guet.commands.start.start_strategy.git_hook_path_from_cwd")
    @patch("guet.commands.start.start_strategy.any_hooks_present")
    def test_execute_if_git_not_present_in_folder_print_error_message(self,
                                                                      mock_any_hooks_present,
                                                                      git_hook_path_from_cwd,
                                                                      mock_create_hook,
                                                                      git_present_in_cwd,
                                                                      mock_print):
        git_present_in_cwd.return_value = False

        command = StartCommandFactory().build([], Settings())
        command.execute()

        mock_print.assert_called_with('Git not initialized in this directory.')

    def test_get_short_help_message(self):
        self.assertEqual('Start guet usage in the repository at current directory',
                         StartCommandFactory().short_help_message())
