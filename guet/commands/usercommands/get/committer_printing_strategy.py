from typing import List, Callable

from guet.commands.strategies.strategy import CommandStrategy
from guet.committers import CommittersPrinter
from guet.committers.committer import Committer


class CommitterPrintingStrategy(CommandStrategy):
    def __init__(self,
                 committers: List[Committer],
                 pre_print_strategy: Callable[[], None],
                 committers_printer: CommittersPrinter):
        self.committers = committers
        self.pre_print_strategy = pre_print_strategy
        self.committers_printer = committers_printer

    def apply(self):
        self.pre_print_strategy()
        self.committers_printer.print(self.committers)
