from typing import List

from guet.committers import CurrentCommitters
from guet.steps.action import Action


class PreCommit(Action):
    def __init__(self, current: CurrentCommitters):
        super().__init__()
        self.current = current

    def execute(self, args: List[str]):
        if len(self.current.get()) == 0:
            print('You must set your pairs before you can commit.')
            exit(1)
