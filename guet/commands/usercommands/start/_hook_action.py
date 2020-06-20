from guet.git.git import Git

from guet.commands.strategies.strategy import CommandStrategy


class HookAction(CommandStrategy):
    def __init__(self, git: Git):
        self.git = git

    def apply(self):
        self._hook_apply()
        self._after_hook_applied()

    def _after_hook_applied(self):
        print('guet successfully started in this repository.')

    def _hook_apply(self) -> None:
        raise NotImplementedError
