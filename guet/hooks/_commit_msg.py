from typing import List

from guet.steps.action import Action

from guet.committers.committer import Committer
from guet.committers.committers import Committers
from guet.git import Git


class CommitMsg(Action):
    def __init__(self, committers: Committers, git: Git):
        super().__init__()
        self.committers = committers
        self.git = git

    def execute(self, _):
        self.git.commit_msg = self._co_autor_lines(self.committers.current())

    def _co_autor_lines(self, committers: List[Committer]) -> List[str]:
        return [f'Co-authored-by: {committer.name} <{committer.email}>' for committer in committers]
