from guet.commands.usercommands.start.hook_strategy import HookStrategy
from guet.git.git import Git


class CreateAlongsideHookStrategy(HookStrategy):
    def apply(self):
        git_path = self.git_path.replace('/hooks', '')
        git = Git(git_path)
        git.create_hooks(alongside=True)
