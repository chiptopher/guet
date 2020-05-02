from guet.commands.usercommands.start.hook_strategy import HookStrategy


class CreateAlongsideHookStrategy(HookStrategy):
    def apply(self):
        self.git.create_hooks(alongside=True)
