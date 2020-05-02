from guet.git.git import Git

from guet.commands.strategies.strategy import CommandStrategy


class HookStrategy(CommandStrategy):
    def __init__(self, git: Git):
        self.git = git

    def apply(self):
        raise NotImplementedError
