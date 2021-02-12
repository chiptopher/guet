from typing import List

from guet.constants import COMMITTERS
from guet.files import File, FileSystem
from guet.util import project_root

from ._committers2_state import Committers2State
from ._global_committer_state import GlobalCommittersState
from .committer import Committer


class LocalCommittersState(Committers2State):
    def __init__(self, file_system: FileSystem, global_state: GlobalCommittersState):
        super().__init__()
        self.file_system = file_system
        self.global_state = global_state

    def all(self) -> List[Committer]:
        local_committers = self._all_local_committers()
        global_committers = self._remove_globals_with_initials_in_local(
            self.global_state.all(), local_committers)

        return global_committers + local_committers

    def add(self, committer: Committer):
        if self.global_state.by_initials(committer.initials):
            print(f'Adding committer with initials "{committer.initials}" '
                  'will overshadow global committer with same initials.')
        if self._local_committer_present(committer.initials):
            self.remove(committer.initials)
        all_committers = self._all_local_committers()
        all_committers.append(committer)
        lines = [str(c) for c in all_committers]
        self._get_committers_file().write(lines)
        self._get_committers_file().save()

    def remove(self, initials: str):
        all_committers = self._all_local_committers()
        without_given = [c for c in all_committers if c.initials != initials]
        lines = [str(c) for c in without_given]
        self._get_committers_file().write(lines)
        self._get_committers_file().save()

    def _get_committers_file(self) -> File:
        pass

    def _all_local_committers(self):
        return [self._map_line_to_committer(c) for c in self._get_committers_file().read()]

    def _remove_globals_with_initials_in_local(self, global_committers, local_committers):
        local_initials = [committer.initials for committer in local_committers]
        return [c for c in global_committers if c.initials not in local_initials]

    def _local_committer_present(self, initials) -> bool:
        try:
            return next((c for c in self._all_local_committers() if c.initials == initials))
        except StopIteration:
            return None

    def _get_committers_file(self) -> File:
        comitters_file_patah = project_root().joinpath('.guet').joinpath(COMMITTERS)
        return self.file_system.get(comitters_file_patah)
