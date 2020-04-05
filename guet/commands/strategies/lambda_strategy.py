from typing import Callable

from guet.commands.strategies.strategy import CommandStrategy


class LambdaStrategy(CommandStrategy):

    def __init__(self, apply: Callable):
        self._apply = apply

    def apply(self):
        self._apply()
