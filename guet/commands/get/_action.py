from typing import List

from guet.committers import Committers2 as Committers
from guet.committers import CommittersPrinter, CurrentCommitters
from guet.steps.action import Action


class GetCommittersAction(Action):

    def __init__(self,
                 committers: Committers,
                 current_committers: CurrentCommitters):
        super().__init__()
        self.committers = committers
        self.current = current_committers

    def execute(self, args: List[str]):
        printer = CommittersPrinter(initials_only=False)
        if args[0] == 'all':
            committers = self.committers.all()
            pre_print = 'All committers'
        else:
            committers = self.current.get()
            pre_print = 'Current committers'

        print(pre_print)
        printer.print(committers)
