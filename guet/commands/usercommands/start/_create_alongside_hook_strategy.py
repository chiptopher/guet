from guet.commands.usercommands.start._hook_action import HookAction


class CreateAlongsideHookAction(HookAction):
    def _hook_apply(self) -> None:
        self.git.create_hooks(alongside=True)
