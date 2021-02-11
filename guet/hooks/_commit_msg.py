from typing import List

from guet.committers import CurrentCommitters
from guet.committers.committer import Committer
from guet.git import Git
from guet.steps.action import Action


class CommitMsg(Action):
    def __init__(self, current_committers: CurrentCommitters, git: Git):
        super().__init__()
        self.current_committers = current_committers
        self.git = git

    def execute(self, _):
        lines = self._co_autor_lines(self.current_committers.get())
        self.git.commit_msg = lines

    def _co_autor_lines(self, committers: List[Committer]) -> List[str]:
        return [f'Co-authored-by: {committer.name} <{committer.email}>' for committer in committers]
