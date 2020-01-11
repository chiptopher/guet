from typing import List

from guet.commands.do_nothing_strategy import DoNothingStrategy
from guet.commands.start.create_hook_strategy import CreateHookStrategy
from guet.commands.strategy import CommandStrategy
from guet.git.hook_mode import HookMode
from guet.git.any_hooks_present import any_hooks_present
from guet.git.create_hook import create_hook, Hooks
from guet.git.git_path_from_cwd import git_hook_path_from_cwd
from guet.git.git_present_in_cwd import git_present_in_cwd
from guet.settings.settings import Settings


class PromptUserForHookTypeStrategy(CommandStrategy):

    def apply(self):
        if git_present_in_cwd():
            hook_path = git_hook_path_from_cwd()
            if not any_hooks_present(hook_path):
                CreateHookStrategy(hook_path).apply()
            else:
                print(('There is already commit hooks in this project. ' +
                       'Would you like to overwrite (o), ' +
                       'create (c) the file and put it in the hooks folder, or cancel (x)?'))
                val = input()
                if val == 'o' or val == 'c':
                    CreateHookStrategy(hook_path).apply()
                else:
                    DoNothingStrategy().apply()

        else:
            print('Git not initialized in this directory.')
