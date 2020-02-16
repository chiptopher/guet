from os.path import join
from typing import List

from guet.git.errors import NotGuetHookError
from guet.git.hook import Hook

GUET_HOOKS = [
    'pre-commit',
    'post-commit',
    'commit-msg'
]


class Git:

    def __init__(self, path_to_repository: str):
        self.hooks = self._load_hooks(path_to_repository)

    def hooks_present(self) -> bool:
        names_of_present_hooks = [hook.path.split('/')[-1] for hook in self.hooks]
        all_present = GUET_HOOKS == names_of_present_hooks
        if not all_present:
            dash_guet = [hook + '-guet' for hook in GUET_HOOKS]
            return dash_guet == names_of_present_hooks
        else:
            return all_present

    def _load_hooks(self, path_to_repository) -> List[Hook]:
        hooks = []
        for hook_name in GUET_HOOKS:
            self._load_hook(hook_name, hooks, path_to_repository)
        return hooks

    def _load_hook(self, hook_name, hooks, path_to_repository):
        hook_path = join(path_to_repository, 'hooks', hook_name)
        try:
            hooks.append(Hook(hook_path))
        except (NotGuetHookError, FileNotFoundError):
            try:
                hooks.append(Hook(hook_path + '-guet'))
            except FileNotFoundError:
                pass
