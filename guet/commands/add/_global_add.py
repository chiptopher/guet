from typing import List

from guet.committers import GlobalCommitter
from guet.committers.committers import Committers
from guet.steps.action import Action


class AddCommittersGlobally(Action):

    def __init__(self, committers: Committers):
        super().__init__()
        self.committers = committers

    def execute(self, args: List[str]):
        initials, name, email = args
        self.committers.add(GlobalCommitter(name, email, initials))
