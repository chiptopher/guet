from typing import List

from guet.commands.strategy import CommandStrategy
from guet.settings.settings import Settings


class InvalidIdentifierStrategy(CommandStrategy):
    def __init__(self, invalid_identifier: str):
        self._invalid_identifier = invalid_identifier

    def apply(self):
        print(f'Invalid identifier <{self._invalid_identifier}>')
