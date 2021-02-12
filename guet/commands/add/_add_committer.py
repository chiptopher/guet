from typing import List

from guet.committers import Committers2 as Committers
from guet.committers.committer import Committer
from guet.steps.action import Action
from guet.util import Args


class AddCommitter(Action):

    def __init__(self, committers: Committers):
        super().__init__()
        self.committers = committers

    def execute(self, args: List[str]):
        initials, name, email = Args(args).without_flags
        self.committers.add(Committer(name, email, initials))
