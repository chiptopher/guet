from pathlib import Path
from typing import List

from guet.committers.committers import Committers
from guet.committers.local_committer import LocalCommitter
from guet.steps.action.action import Action


class LocalAddCommitter(Action):
    def __init__(self, committers: Committers, project_root: Path):
        self._committers = committers
        self._project_root = project_root

    def execute(self, args: List[str]):
        args = [arg for arg in args if not arg.startswith('-')]
        initials, name, email = args
        committer = LocalCommitter(
            initials='initials', name='name', email='emai', project_root=self._project_root)

        self._committers.add(committer)
