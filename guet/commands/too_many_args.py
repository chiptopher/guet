from typing import List

from guet.settings.settings import Settings
from guet.commands.strategy_command import CommandStrategy


class TooManyArgsStrategy(CommandStrategy):
    def apply(self, args: List[str], settings: Settings()):
        print('Too many arguments.')