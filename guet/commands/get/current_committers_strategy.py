from typing import List

from guet.commands.get.committer_printing_strategy import CommitterPrintingStrategy
from guet.commands.strategy_command import CommandStrategy
from guet.settings.settings import Settings


class CurrentCommittersStrategy(CommandStrategy):
    def __init__(self, committer_printing_strategy: CommitterPrintingStrategy):
        self.committer_printing_strategy = committer_printing_strategy

    def apply(self, args: List[str], settings: Settings):
        print('Currently set committers')
        self.committer_printing_strategy.apply(args, settings)
