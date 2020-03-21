from os import mkdir
from os.path import isdir, join

from guet.commands.strategy import CommandStrategy
from guet.committers.local_committer import LocalCommitter
from guet.config.committers import Committers


class AddCommitterLocallyStrategy(CommandStrategy):
    def __init__(self, initials: str, name: str, email: str, project_root: str, committers: Committers):
        self._initials = initials
        self._name = name
        self._email = email
        self._project_root = project_root
        self._committers = committers

    def apply(self) -> None:
        self._create_local_guet_folder_if_not_exists()
        committer = LocalCommitter(name=self._name, email=self._email, initials=self._initials,
                                   project_root=self._project_root)
        self._committers.add(committer)

    def _create_local_guet_folder_if_not_exists(self) -> None:
        folder_path = join(self._project_root, '.guet')
        if not isdir(folder_path):
            mkdir(folder_path)
