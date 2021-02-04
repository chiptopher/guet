from typing import List

from guet.committers import LocalCommitter
from guet.committers.committers import Committers
from guet.steps.action import Action
from guet.util import Args, project_root


class AddCommittersLocally(Action):

    def __init__(self, committers: Committers):
        super().__init__()
        self.committers = committers

    def execute(self, args: List[str]):
        initials, name, email = Args(args).without_flags
        self.committers.add(LocalCommitter(name, email, initials, project_root=project_root()))
