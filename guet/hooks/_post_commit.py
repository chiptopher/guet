from typing import List

from guet.committers import CurrentCommitters
from guet.steps.action import Action


class PostCommit(Action):
    def __init__(self, current_committers: CurrentCommitters):
        super().__init__()
        self.current_committers = current_committers

    def execute(self, args: List[str]):
        found = self.current_committers.get()
        if len(found) > 1:
            first = found.pop(0)
            found.append(first)
            self.current_committers.set(found)
