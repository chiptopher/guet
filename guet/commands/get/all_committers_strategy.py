from typing import List

from guet.commands.strategy_command import CommandStrategy
from guet.settings.settings import Settings


class AllCommittersStrategy(CommandStrategy):
    def __init__(self, committer_printing_strategy):
        self.committer_printing_strategy = committer_printing_strategy

    def apply(self, args: List[str], settings: Settings):
        print('All committers')
        self.committer_printing_strategy.apply(args, settings)
