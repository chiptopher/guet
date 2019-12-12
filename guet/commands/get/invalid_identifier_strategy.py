from typing import List

from guet.commands.strategy_command import CommandStrategy
from guet.settings.settings import Settings


class InvalidIdentifierStrategy(CommandStrategy):
    def apply(self, args: List[str], settings: Settings):
        print(f'Invalid identifier <{args[0]}>')
