from typing import List

from guet.committers.committer import Committer
from guet.committers.committers import Committers
from guet.git import Git
from guet.steps.action import Action


class PreCommit(Action):
    def __init__(self, committers: Committers):
        super().__init__()
        self.committers = committers

    def execute(self, args: List[str]):
        if len(self.committers.current()) == 0:
            print('You must set your pairs before you can commit.')
            exit(1)
