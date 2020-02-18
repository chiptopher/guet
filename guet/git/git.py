from os.path import join
from typing import List

from guet.git.errors import NotGuetHookError
from guet.git.hook import Hook

GUET_HOOKS = [
    'pre-commit',
    'post-commit',
    'commit-msg'
]


class _FileNameStrategy:
    def apply(self, base_name: str) -> str:
        raise NotImplementedError()


class _AlongsideFileNameStrategy(_FileNameStrategy):
    def apply(self, base_name: str):
        return base_name + '-guet'


class _BaseFileNameStrategy(_FileNameStrategy):
    def apply(self, base_name: str) -> str:
        return base_name


class _CreateStrategy:
    def apply(self):
        raise NotImplementedError()


class _DoCreateStrategy(_CreateStrategy):
    def apply(self):
        return True


class _DontCreateStrategy(_CreateStrategy):
    def apply(self):
        return False


class _HookLoader:
    def __init__(self, path_to_repository, file_name: _FileNameStrategy, create: _CreateStrategy):
        self.create = create
        self.file_name = file_name
        self.path_to_repository = path_to_repository

    def apply(self, hook_name: str, hooks: List[Hook]):
        hook_path = join(self.path_to_repository, 'hooks', self.file_name.apply(hook_name))
        try:
            hooks.append(Hook(hook_path, create=self.create.apply()))
        except (FileNotFoundError, NotGuetHookError):
            pass


def _load_hooks(hook_strategy: _HookLoader) -> List[Hook]:
    hooks = []
    for hook_name in GUET_HOOKS:
        hook_strategy.apply(hook_name, hooks)
    return hooks


def _default_hooks_present(present_hooks: List[str]) -> bool:
    return GUET_HOOKS == present_hooks


def _alongside_hooks_present(present_hooks: List[str]) -> bool:
    dash_guet = [hook + '-guet' for hook in GUET_HOOKS]
    return dash_guet == present_hooks


def _check_for_alongside_hooks_if_they_dont_exist_already() -> List[Hook]:
    pass


class Git:

    def __init__(self, repository_path: str):
        default = _load_hooks(_HookLoader(repository_path, _BaseFileNameStrategy(), _DontCreateStrategy()))
        alongside = _load_hooks(_HookLoader(repository_path, _AlongsideFileNameStrategy(), _DontCreateStrategy()))
        self.hooks = default + alongside
        self.path_to_repository = repository_path

    def hooks_present(self) -> bool:
        names_of_present_hooks = [hook.path.split('/')[-1] for hook in self.hooks]
        default_hooks_present = _default_hooks_present(names_of_present_hooks)
        alongside_hooks_present = _alongside_hooks_present(names_of_present_hooks)
        return default_hooks_present or alongside_hooks_present

    def create_hooks(self, alongside=False) -> None:
        if alongside:
            hook_loader = _HookLoader(self.path_to_repository, _AlongsideFileNameStrategy(), _DoCreateStrategy())
        else:
            hook_loader = _HookLoader(self.path_to_repository, _BaseFileNameStrategy(), _DoCreateStrategy())
        self.hooks = _load_hooks(hook_loader)
        for hook in self.hooks:
            hook.save()
