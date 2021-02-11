from typing import List

from guet.steps.check.check import Check


class HelpCheck(Check):

    def __init__(self, stop_message, *, stop_on_no_args=False):
        super().__init__(stop_message)
        self.stop_on_no_args = stop_on_no_args

    def should_stop(self, args: List[str]) -> bool:
        return '--help' in args or '-h' in args or self._should_stop_for_empty_args(args)

    def _should_stop_for_empty_args(self, args: List[str]) -> bool:
        if self.stop_on_no_args:
            return len(args) == 0
        return False
