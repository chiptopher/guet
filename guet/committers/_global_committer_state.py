from typing import List

from guet.constants import COMMITTERS
from guet.files import File, FileSystem

from ._committers2_state import Committers2State
from .committer import Committer


class GlobalCommittersState(Committers2State):
    def __init__(self, file_system: FileSystem):
        super().__init__()
        self.file_system = file_system

    def all(self) -> List[Committer]:
        return [self._map_line_to_committer(c) for c in self._get_committers_file().read()]

    def add(self, committer: Committer):
        if self.by_initials(committer.initials):
            self.remove(committer.initials)
        all_committers = self.all()
        all_committers.append(committer)
        lines = [str(c) for c in all_committers]
        self._get_committers_file().write(lines)
        self._get_committers_file().save()

    def remove(self, initials: str):
        all_committers = self.all()
        without_given = [c for c in all_committers if c.initials != initials]
        lines = [str(c) for c in without_given]
        self._get_committers_file().write(lines)
        self._get_committers_file().save()

    def _get_committers_file(self) -> File:
        comitters_file_patah = FileSystem.config_directory().joinpath(COMMITTERS)
        return self.file_system.get(comitters_file_patah)
