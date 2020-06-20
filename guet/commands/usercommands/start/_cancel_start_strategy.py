from guet.commands.usercommands.start._hook_action import HookAction


class CancelStartAction(HookAction):
    def _hook_apply(self) -> None:
        pass

    def _after_hook_applied(self) -> None:
        print('guet not started.')
