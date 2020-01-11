from guet.commands.start.hook_strategy import HookStrategy
from guet.git.hook_mode import HookMode
from guet.git.create_hook import Hooks, create_hook


class CreateHookStrategy(HookStrategy):
    def apply(self):
        create_hook(self._hook_path, Hooks.PRE_COMMIT, HookMode.NEW_OR_OVERWRITE)
        create_hook(self._hook_path, Hooks.POST_COMMIT, HookMode.NEW_OR_OVERWRITE)
        create_hook(self._hook_path, Hooks.COMMIT_MSG, HookMode.NEW_OR_OVERWRITE)
