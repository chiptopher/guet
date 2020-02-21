from guet.commands.start.hook_strategy import HookStrategy
from guet.git.git import Git


class CreateHookStrategy(HookStrategy):
    def apply(self):
        git_path = self.git_path.replace('/hooks', '')
        git = Git(git_path)
        git.create_hooks()
