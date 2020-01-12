from guet.commands.start.hook_strategy import HookStrategy
from guet.git.create_hook import create_hook, Hooks
from guet.git.hook_mode import HookMode


class CreateAlongsideHookStrategy(HookStrategy):
    def apply(self):
        create_hook(self._hook_path, Hooks.PRE_COMMIT, HookMode.CREATE_ALONGSIDE)
        create_hook(self._hook_path, Hooks.POST_COMMIT, HookMode.CREATE_ALONGSIDE)
        create_hook(self._hook_path, Hooks.COMMIT_MSG, HookMode.CREATE_ALONGSIDE)
