from guet.commands.strategy import CommandStrategy


class HookStrategy(CommandStrategy):
    def __init__(self, git_path: str):
        self.git_path = git_path

    def apply(self):
        raise NotImplementedError
