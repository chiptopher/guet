from pathlib import Path
from typing import List
from guet.steps.action.action import Action
from guet.committers.committers import Committers
from guet.committers.global_committer import GlobalCommitter


class GlobalAddCommitter(Action):
    def __init__(self, committers: Committers):
        self._committers = committers

    def execute(self, args: List[str]):
        args = [arg for arg in args if not arg.startswith('-')]
        initials, name, email = args
        committer = GlobalCommitter(
            initials='initials', name='name', email='emai')

        self._committers.add(committer)
