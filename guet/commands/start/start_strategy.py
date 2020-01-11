from typing import List

from guet.commands.do_nothing_strategy import DoNothingStrategy
from guet.commands.start.create_hook_strategy import CreateHookStrategy
from guet.commands.start.hook_strategy import HookStrategy


class PromptUserForHookTypeStrategy(HookStrategy):
    def apply(self):
        print(('There is already commit hooks in this project. ' +
               'Would you like to overwrite (o), ' +
               'create (c) the file and put it in the hooks folder, or cancel (x)?'))
        val = input()
        if val == 'o' or val == 'c':
            CreateHookStrategy(self._hook_path).apply()
        else:
            DoNothingStrategy().apply()
