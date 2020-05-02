from pathlib import Path

from guet import constants
from guet.committers._add_committer import add_committer
from guet.committers.committer import Committer


class LocalCommitter(Committer):
    def __init__(self, name: str, email: str, initials: str, project_root: Path):
        super().__init__(name, email, initials)
        self._project_root = project_root

    def save(self):
        path = self._project_root.joinpath('.guet').joinpath(constants.COMMITTERS)
        add_committer(self.initials, self.name, self.email, file_path=path)
