from typing import List

from guet.context.context import Context
from guet.committers import CommittersPrinter
from guet.committers.committers import Committers
from guet.steps.action import Action


class SetCommittersAction(Action):
    def __init__(self, committers: Committers, context: Context):
        super().__init__()
        self.committers = committers
        self.context = context

    def execute(self, args: List[str]):
        lowercase_args = [arg.lower() for arg in args]
        found = [c for c in self.committers.all() if c.initials in lowercase_args]
        self.context.set_committers(found)

        printer = CommittersPrinter(initials_only=False)
        print('Committers set to:')
        printer.print(found)
