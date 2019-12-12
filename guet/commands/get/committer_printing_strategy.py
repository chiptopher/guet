from typing import List

from guet.commands.strategy_command import CommandStrategy
from guet.config.committer import Committer
from guet.settings.settings import Settings


class CommitterPrintingStrategy(CommandStrategy):
    def __init__(self, committers: List[Committer]):
        self.committers = committers

    def apply(self, args: List[str], settings: Settings):
        raise NotImplementedError
