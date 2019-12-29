from typing import List, Callable

from guet.commands.strategy import CommandStrategy
from guet.settings.settings import Settings


class LambdaStrategy(CommandStrategy):

    def __init__(self, apply: Callable):
        self._apply = apply

    def apply(self):
        self._apply()
