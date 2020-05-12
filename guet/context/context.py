from os import mkdir
from os.path import join
from pathlib import Path
from typing import List, Union

from guet import constants, __version__
from guet.config import CONFIGURATION_DIRECTORY

from guet.committers.committer import Committer
from guet.committers.committers import Committers
from guet.config.errors import AlreadyInitializedError
from guet.context.set_committers_observable import SetCommittersObservable
from guet.files import FileSystem, File
from guet.git.git import Git
from guet.context.errors import InvalidCommittersError
from guet.util import project_root


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
        return Context(None, file_system=FileSystem())

    def __init__(self, project_root_directory: Union[Path, None], *, file_system: FileSystem):
        super().__init__()
        self._committers: Union[Committers, None] = None
        self._git = None
        self._project_root_directory = project_root_directory
        self._file_system: Union[FileSystem, None] = file_system

    @property
    def project_root_directory(self) -> Path:
        if self._project_root_directory is None:
            root = project_root()
            self._project_root_directory = root.absolute()
        return self._project_root_directory

    @project_root_directory.setter
    def project_root_directory(self, new: str) -> None:
        self._project_root_directory = new

    @property
    def committers(self):
        if self._committers is None:
            try:
                project_dir = self.project_root_directory
            except FileNotFoundError:
                project_dir = None
            self._committers = Committers(path_to_project_root=project_dir)
            self.add_set_committer_observer(self._committers)
        return self._committers

    @committers.setter
    def committers(self, new_committers):
        self._committers = new_committers

    @property
    def git(self):
        if self._git is None:
            self._git = Git(self.project_root_directory.joinpath('.git'))
            self.add_set_committer_observer(self._git)
        return self._git

    @_attempt_to_load_committers
    @_attempt_to_load_git
    def set_committers(self, committers: List[Committer]):
        if len(committers) > 0:
            self.notify_set_committer_observers(committers)
        else:
            raise InvalidCommittersError()

    def _create_empty(self, path: Path) -> File:
        return self._file_system.get(path)

    def initialize(self):
        self._create_configuration_directory()

        self._create_empty(Path(join(CONFIGURATION_DIRECTORY, constants.COMMITTER_NAMES))).read()
        self._create_empty(Path(join(CONFIGURATION_DIRECTORY, constants.COMMITTERS))).read()
        self._create_empty(Path(join(CONFIGURATION_DIRECTORY, constants.COMMITTERS_SET))).read()
        self._create_empty(Path(join(CONFIGURATION_DIRECTORY, constants.ERRORS))).read()

        config = self._create_empty(Path(join(CONFIGURATION_DIRECTORY, constants.CONFIG)))
        config.write([f'{__version__}\n', '\n'])

        self._file_system.save_all()

    def _create_configuration_directory(self):
        try:
            mkdir(CONFIGURATION_DIRECTORY)
        except FileExistsError:
            raise AlreadyInitializedError()
