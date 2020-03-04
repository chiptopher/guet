from os import getcwd
from os.path import join
from typing import List

from guet.config.committer import Committer
from guet.config.committers import Committers
from guet.context.set_committers_observable import SetCommittersObservable
from guet.git.git import Git
from guet.context.errors import InvalidCommittersError


def _attempt_to_load_git(f):
    def wrapper(*args, **kwargs):
        context: Context = args[0]
        context.git
        return f(*args, **kwargs)

    return wrapper


def _attempt_to_load_committers(f):
    def wrapper(*args, **kwargs):
        context: Context = args[0]
        context.committers
        return f(*args, **kwargs)

    return wrapper


class Context(SetCommittersObservable):
    @staticmethod
    def instance(*, load_git: bool = False):
        return Context(getcwd(), load_git=load_git)

    def __init__(self, project_root_directory: str, *, load_git: bool = True):
        super().__init__()
        self._load_git = load_git
        self._committers = None
        self._git = None
        self.project_root_directory = project_root_directory

    @property
    def committers(self):
        if self._committers is None:
            self._committers = Committers()
            self.add_set_committer_observer(self._committers)
        return self._committers

    @property
    def git(self):
        if self._git is None and self._load_git:
            self._git = Git(join(self.project_root_directory, '.git'))
            self.add_set_committer_observer(self._git)
        return self._git

    @_attempt_to_load_committers
    @_attempt_to_load_git
    def set_committers(self, committers: List[Committer]):
        if len(committers) > 0:
            self.notify_set_committer_observers(committers)
        else:
            raise InvalidCommittersError()
