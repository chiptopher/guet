from typing import List

from guet.steps.check import Check
from guet.util import Args


class ArgumentCheck(Check):

    def __init__(self):
        super().__init__()

    def should_stop(self, args: List[str]) -> bool:
        return self.not_enough_args(args) or self.too_many_args(args)

    def load_message(self, args: List[str]) -> str:
        if self.not_enough_args(args):
            return 'Not enough arguments.'
        else:
            return 'Too many arguments.'

    def not_enough_args(self, args: List[str]) -> bool:
        return len(Args(args).without_flags) < 3

    def too_many_args(self, args: List[str]) -> bool:
        return len(Args(args).without_flags) > 3
