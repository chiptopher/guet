from typing import List
from guet.steps.check.check import Check
from guet import __version__ as version


class VersionCheck(Check):

    def __init__(self):
        super().__init__(version)

    def should_stop(self, args: List[str]) -> bool:
        return '--version' in args or '-v' in args
