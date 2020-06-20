from guet.commands.usercommands.start.hook_strategy import HookStrategy


class CancelStartStrategy(HookStrategy):
    def _hook_apply(self) -> None:
        pass

    def _after_hook_applied(self) -> None:
        print('guet not started.')
