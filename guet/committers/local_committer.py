from os.path import join

from guet import constants
from guet.config.add_committer import add_committer
from guet.config.committer import Committer


class LocalCommitter(Committer):
    def __init__(self, name: str, email: str, initials: str, project_root: str):
        super().__init__(name, email, initials)
        self._project_root = project_root

    def save(self):
        path = join(self._project_root, '.guet', constants.COMMITTERS)
        add_committer(self.initials, self.name, self.email, file_path=path)
