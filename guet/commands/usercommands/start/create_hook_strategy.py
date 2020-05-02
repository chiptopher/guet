from guet.commands.usercommands.start.hook_strategy import HookStrategy


class CreateHookStrategy(HookStrategy):
    def apply(self):
        self.git.create_hooks()
