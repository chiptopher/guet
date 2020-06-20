from guet.commands.usercommands.start._cancel_start_strategy import CancelStartAction
from guet.commands.usercommands.start._create_alongside_hook_strategy import CreateAlongsideHookAction
from guet.commands.usercommands.start._create_hook_strategy import CreateHookAction
from guet.commands.usercommands.start._hook_action import HookAction


class PromptUserForHookTypeAction(HookAction):
    def _hook_apply(self) -> None:
        print('There is already commit hooks in this project. You can')
        print('  (o) overwrite current hooks. This will delete any matching hooks.')
        print(('  (a) create guet hooks alongside current ones.'
               'This will create them with \'-guet\' appended on the name of the hook file.'))
        print('  (x) cancel the request. This will do nothing.')
        val = input()
        if val == 'o':
            CreateHookAction(self.git).apply()
        elif val == 'a':
            CreateAlongsideHookAction(self.git).apply()
        else:
            CancelStartAction(self.git).apply()

    def _after_hook_applied(self):
        pass
