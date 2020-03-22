from os import getcwd
from os.path import join
from typing import List

from guet.config.committer import Committer
from guet.config.committers import Committers
from guet.context.set_committers_observable import SetCommittersObservable
from guet.git.git import Git
from guet.context.errors import InvalidCommittersError


def _attempt_to_load_git(function):
    def wrapper(*args, **kwargs):
        context: Context = args[0]
        context.__getattribute__('git')
        return function(*args, **kwargs)

    return wrapper


def _attempt_to_load_committers(function):
    def wrapper(*args, **kwargs):
        context: Context = args[0]
        context.__getattribute__('committers')
        return function(*args, **kwargs)

    return wrapper


class Context(SetCommittersObservable):
    @staticmethod
    def instance():
        return Context(getcwd())

    def __init__(self, project_root_directory: str):
        super().__init__()
        self._committers: Committers = None
        self._git = None
        self.project_root_directory = project_root_directory

    @property
    def committers(self):
        if self._committers is None:
            self._committers = Committers(path_to_project_root=self.project_root_directory)
            self.add_set_committer_observer(self._committers)
        return self._committers

    @committers.setter
    def committers(self, new_committers):
        self._committers = new_committers

    @property
    def git(self):
        if self._git is None:
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
