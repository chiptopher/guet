from typing import List

from guet.commands.strategy import CommandStrategy
from guet.settings.settings import Settings


class PrintCommandStrategy(CommandStrategy):
    def __init__(self, text: str):
        self._text = text

    def apply(self):
        print(self._text)
