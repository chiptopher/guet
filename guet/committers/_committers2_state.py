from typing import List

from .committer import Committer


class Committers2State:
    def all(self) -> List[Committer]:
        raise NotImplementedError

    def by_initials(self, initials: str) -> Committer:
        try:
            return next(c for c in self.all() if c.initials == initials)
        except StopIteration:
            return None

    def add(self, committer: Committer):
        raise NotImplementedError

    def remove(self, initials: str):
        raise NotImplementedError

    def _map_line_to_committer(self, line: str) -> Committer:
        initials, name, email = line.split(',')
        return Committer(initials=initials, name=name, email=email)
