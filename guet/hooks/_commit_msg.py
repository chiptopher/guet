from typing import List

from guet.committers import CurrentCommitters
from guet.committers.committer import Committer
from guet.git import Git, append_committers
from guet.steps.action import Action


class CommitMsg(Action):
    def __init__(self, current_committers: CurrentCommitters, git: Git):
        super().__init__()
        self.current_committers = current_committers
        self.git = git

    def execute(self, _):
        new_lines = append_committers(self.current_committers.get(), self.git.commit_msg)
        self.git.commit_msg = new_lines

    def _co_autor_lines(self, committers: List[Committer]) -> List[str]:
        return [f'Co-authored-by: {committer.name} <{committer.email}>' for committer in committers]
