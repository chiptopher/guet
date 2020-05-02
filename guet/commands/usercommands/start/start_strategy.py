from guet.commands.strategies.do_nothing_strategy import DoNothingStrategy
from guet.commands.usercommands.start.create_alongside_hook_strategy import CreateAlongsideHookStrategy
from guet.commands.usercommands.start.create_hook_strategy import CreateHookStrategy
from guet.commands.usercommands.start.hook_strategy import HookStrategy


class PromptUserForHookTypeStrategy(HookStrategy):
    def _hook_apply(self) -> None:
        print('There is already commit hooks in this project. You can')
        print('  (o) overwrite current hooks. This will delete any matching hooks.')
        print(('  (a) create guet hooks alongside current ones.'
               'This will create them with \'-guet\' appended on the name of the hook file.'))
        print('  (x) cancel the request. This will do nothing.')
        val = input()
        if val == 'o':
            CreateHookStrategy(self.git).apply()
        elif val == 'a':
            CreateAlongsideHookStrategy(self.git).apply()
        else:
            DoNothingStrategy().apply()
