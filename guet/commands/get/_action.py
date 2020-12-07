from typing import List

from guet.committers import CommittersPrinter
from guet.committers.committers import Committers
from guet.steps.action import Action


class GetCommittersAction(Action):

    def __init__(self, committers: Committers):
        super().__init__()
        self.committers = committers

    def execute(self, args: List[str]):
        printer = CommittersPrinter(initials_only=False)
        if args[0] == 'all':
            committers = self.committers.all()
            pre_print = 'All committers'
        else:
            committers = self.committers.current()
            pre_print = 'Current committers'

        print(pre_print)
        printer.print(committers)
