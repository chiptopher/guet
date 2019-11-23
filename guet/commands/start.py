from typing import List

from guet.commands.command import Command
from guet.git.any_hooks_present import any_hooks_present
from guet.git.create_hook import create_hook, HookMode, Hooks
from guet.git.git_path_from_cwd import git_hook_path_from_cwd
from guet.git.git_present_in_cwd import git_present_in_cwd
from guet.settings.settings import Settings


class StartCommand(Command):
    def __init__(self, args: List[str], settings: Settings):
        super().__init__(args, settings, args_needed=False)

    def execute_hook(self) -> None:
        if git_present_in_cwd():
            hook_path = git_hook_path_from_cwd()
            if not any_hooks_present(hook_path):
                self._create_all_hooks(hook_path, HookMode.NEW_OR_OVERWRITE)
            else:
                hook_mode = None
                print(('There is already commit hooks in this project. ' +
                       'Would you like to overwrite (o), ' +
                       'create (c) the file and put it in the hooks folder, or cancel (x)?'))
                val = input()
                if val == 'o':
                    hook_mode = HookMode.NEW_OR_OVERWRITE
                elif val == 'c':
                    hook_mode = HookMode.CREATE_ALONGSIDE
                else:
                    hook_mode = HookMode.CANCEL
                self._create_all_hooks(hook_path, hook_mode)

        else:
            print('Git not initialized in this directory.')

    @staticmethod
    def _create_all_hooks(hook_folder_path: str, hook_mode: HookMode):
        if hook_mode is not HookMode.CANCEL:
            create_hook(hook_folder_path, Hooks.PRE_COMMIT, hook_mode)
            create_hook(hook_folder_path, Hooks.POST_COMMIT, hook_mode)
            create_hook(hook_folder_path, Hooks.COMMIT_MSG, hook_mode)

    def help(self):
        pass

    @classmethod
    def help_short(cls) -> str:
        return 'Start guet usage in the repository at current directory'
