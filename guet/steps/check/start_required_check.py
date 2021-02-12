from typing import List

from guet.git.git import Git
from guet.steps.check.check import Check
from guet.util import project_root

GUET_NOT_STARTED_ERROR = (
    'guet not initialized in this repository. '
    'Please use guet start to initialize repository '
    'for use with guet.'
)


class StartRequiredCheck(Check):
    def __init__(self):
        super().__init__(GUET_NOT_STARTED_ERROR)

    def should_stop(self, args: List[str]) -> bool:
        git = Git(project_root().joinpath('.git'))
        return not git.hooks_present()
