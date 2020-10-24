from typing import List
from guet.steps.check.check import Check


class HelpCheck(Check):

    def should_stop(self, args: List[str]) -> bool:
        return '--help' in args or '-h' in args
