from typing import List

from guet.commands.strategy import CommandStrategy
from guet.settings.settings import Settings


class HelpMessageStrategy(CommandStrategy):
    def __init__(self, help_message: str):
        self.help_message = help_message

    def apply(self):
        print(self.help_message)
