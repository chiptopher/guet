from typing import List
from pathlib import Path
from guet.steps.check.check import Check
from guet.git.git import Git

GUET_NOT_STARTED_ERROR = (
    'guet not initialized in this repository. '
    'Please use guet start to initialize repository '
    'for use with guet.'
)


class StartRequiredCheck(Check):
    def __init__(self, path_to_project_root: Path):
        super().__init__(GUET_NOT_STARTED_ERROR)
        self.path_to_project_root = path_to_project_root

    def should_stop(self, args: List[str]) -> bool:
        git = Git(self.path_to_project_root.joinpath('.git'))
        return not git.hooks_present()
