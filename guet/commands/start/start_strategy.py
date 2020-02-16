from guet.commands.do_nothing_strategy import DoNothingStrategy
from guet.commands.start.create_alongside_hook_strategy import CreateAlongsideHookStrategy
from guet.commands.start.create_hook_strategy import CreateHookStrategy
from guet.commands.start.hook_strategy import HookStrategy


class PromptUserForHookTypeStrategy(HookStrategy):
    def apply(self):
        print(('There is already commit hooks in this project. ' +
               'Would you like to overwrite (o), ' +
               'create (a) the file and put it in the hooks folder, or cancel (x)?'))
        val = input()
        if val == 'o':
            CreateHookStrategy(self._hook_path).apply()
        elif val == 'a':
            CreateAlongsideHookStrategy(self._hook_path).apply()
        else:
            DoNothingStrategy().apply()
