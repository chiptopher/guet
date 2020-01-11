from guet.commands.strategy import CommandStrategy


class HookStrategy(CommandStrategy):
    def __init__(self, hook_path: str):
        self._hook_path = hook_path

    def apply(self):
        raise NotImplementedError
