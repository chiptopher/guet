from typing import List

from guet.committers import Committers2 as Committers
from guet.steps.check import Check


class OverwritingCommitterCheck(Check):

    def __init__(self, committers: Committers):
        super().__init__('')
        self.committers = committers

    def should_stop(self, args: List[str]) -> bool:
        initials, name, email, *_ = args
        found = self.committers.by_initials(args[0])
        if not found:
            return False
        else:
            print((f'Matching initials "{initials}". Adding '
                   f'"{name}" <{email}> will overwrite '
                   f'"{found.name}" <{found.email}>. Would you '
                   'like to continue(y) or cancel(x)?'))

            choice = input()

            if choice == 'x':
                return True
            else:
                self.committers.remove(found.initials)
                return False
