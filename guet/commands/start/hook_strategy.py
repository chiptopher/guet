from guet.commands.strategy import CommandStrategy
from guet.context.context import Context


class HookStrategy(CommandStrategy):
    def __init__(self, git_path: str, context: Context):
        self.git_path = git_path
        self.context = context

    def apply(self):
        raise NotImplementedError
