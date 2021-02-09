from guet.committers.committer import Committer
from guet.files import FileSystem

from ._global_committer_state import GlobalCommittersState
from ._local_committers_state import LocalCommittersState


class Committers:
    def __init__(self, file_system: FileSystem):
        self.global_state = GlobalCommittersState(file_system)
        self.local_state = LocalCommittersState(file_system, self.global_state)

        self.current_state = self.global_state

    def to_local(self):
        self.current_state = self.local_state

    def to_global(self):
        self.current_state = self.global_state

    def all(self):
        def sort_key(committer: Committer):
            return committer.initials
        found = self.current_state.all()
        found.sort(key=sort_key)
        return found

    def by_initials(self, initials: str):
        return self.current_state.by_initials(initials.lower())

    def add(self, committer: Committer):
        self.current_state.add(committer)

    def remove(self, initials: str):
        self.current_state.remove(initials)
