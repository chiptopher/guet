from typing import List, Callable

from guet.commands.strategy import CommandStrategy
from guet.config.committer import Committer


class CommitterPrintingStrategy(CommandStrategy):
    def __init__(self,
                 committers: List[Committer],
                 pre_print_strategy: Callable[[], None],
                 listing_strategy: Callable[[List[Committer]], None]):
        self.committers = committers
        self.pre_print_strategy = pre_print_strategy
        self.listing_strategy = listing_strategy

    def apply(self):
        self.pre_print_strategy()
        self.listing_strategy(self.committers)
