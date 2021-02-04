from typing import List


from guet.committers.committers import Committers
from guet.errors import InvalidInitialsError
from guet.steps.check import Check


class CommittersExistCheck(Check):
    def __init__(self, committers: Committers):
        super().__init__()
        self.committers = committers

    def should_stop(self, args: List[str]) -> bool:
        return len(self._get_missing_committer_initials(args)) > 0

    def load_message(self, args: List[str]) -> str:
        return '\n'.join([f"No committer exists with initials '{initial}'"
                          for initial in
                          self._get_missing_committer_initials(args)])

    def _get_missing_committer_initials(self, args: List[str]) -> List[str]:
        missing = []
        for initial in args:
            try:
                self.committers.by_initials(initial)
            except InvalidInitialsError:
                missing.append(initial)
        return missing