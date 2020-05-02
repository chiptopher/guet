from guet.commands.usercommands.start.hook_strategy import HookStrategy


class CreateAlongsideHookStrategy(HookStrategy):
    def _hook_apply(self) -> None:
        self.git.create_hooks(alongside=True)
