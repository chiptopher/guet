from typing import List

from guet.steps.check import Check


class ArgumentCheck(Check):

    def __init__(self):
        super().__init__()

    def should_stop(self, args: List[str]) -> bool:
        return self.not_enough_args(args)

    def load_message(self, args: List[str]) -> str:
        if self.not_enough_args(args):
            return 'Not enough arguments.'

    def not_enough_args(self, args: List[str]) -> bool:
        return len(args) < 3
