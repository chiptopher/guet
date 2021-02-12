from typing import List

from guet.git import Git
from guet.steps.action import Action


class CreateHooksAlongside(Action):
    def __init__(self, git: Git):
        super().__init__()
        self.git = git

    def execute(self, args: List[str]):
        self.git.create_hooks(alongside=True)
