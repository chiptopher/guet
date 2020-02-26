from os.path import join, isdir
from typing import List

from guet.config.committer import Committer
from guet.context.set_committer_observer import SetCommitterObserver
from guet.files.read_lines import read_lines
from guet.files.write_lines import write_lines
from guet.git._all_valid_hooks import all_valid_hooks
from guet.git._author_manage import load_author, overwrite_current_author, get_author_lines, append_new_author
from guet.git._create_strategy import DoCreateStrategy, DontCreateStrategy
from guet.git._file_name_strategy import BaseFileNameStrategy, AlongsideFileNameStrategy
from guet.git._guet_hooks import GUET_HOOKS
from guet.git._hook_loader import HookLoader
from guet.git.author import Author
from guet.git.errors import NoGitPresentError
from guet.git.hook import Hook


def _load_hooks(hook_strategy: HookLoader) -> List[Hook]:
    hooks = []
    for hook_name in GUET_HOOKS:
        hook_strategy.apply(hook_name, hooks)
    return hooks


def _load_commit_msg(path_to_repository) -> List[str]:
    try:
        return read_lines(join(path_to_repository, 'COMMIT_EDITMSG'))
    except FileNotFoundError:
        return []


class Git(SetCommitterObserver):

    def __init__(self, repository_path: str):
        super().__init__()
        if not isdir(repository_path):
            raise NoGitPresentError()
        default = _load_hooks(HookLoader(repository_path, BaseFileNameStrategy(), DontCreateStrategy()))
        alongside = _load_hooks(HookLoader(repository_path, AlongsideFileNameStrategy(), DontCreateStrategy()))
        self.hooks = default + alongside
        self.path_to_repository = repository_path
        self._commit_msg = _load_commit_msg(repository_path)
        self._config_lines = read_lines(join(repository_path, 'config'))
        self._author: Author = load_author(self._config_lines)

    @property
    def author(self) -> Author:
        return self._author

    @author.setter
    def author(self, new_author: Author):
        new_lines = list(self._config_lines)
        user, email = get_author_lines(self._config_lines)
        if user is not None and email is not None:
            overwrite_current_author(new_lines, new_author)
        else:
            append_new_author(new_lines, new_author)
        write_lines(join(self.path_to_repository, 'config'), new_lines)
        self._author = new_author

    @property
    def commit_msg(self):
        return self._commit_msg

    @commit_msg.setter
    def commit_msg(self, lines: List[str]):
        write_lines(join(self.path_to_repository, 'COMMIT_EDITMSG'), lines)
        self._commit_msg = lines

    def hooks_present(self) -> bool:
        return all_valid_hooks(self.hooks)

    def non_guet_hooks_present(self) -> bool:
        non_guet_hook_found = False
        for hook in self.hooks:
            if not hook.is_guet_hook():
                non_guet_hook_found = True
        return non_guet_hook_found

    def create_hooks(self, alongside: bool = False) -> None:
        if alongside:
            hook_loader = HookLoader(self.path_to_repository, AlongsideFileNameStrategy(), DoCreateStrategy())
        else:
            hook_loader = HookLoader(self.path_to_repository, BaseFileNameStrategy(), DoCreateStrategy())
        self.hooks = _load_hooks(hook_loader)
        for hook in self.hooks:
            hook.save()

    def notify_of_committer_set(self, new_committers: List[Committer]):
        author_committer = new_committers[0]
        self.author = Author(name=author_committer.name, email=author_committer.email)
