from typing import List

from guet.settings.settings import Settings
from guet.commands.command import Command


class CommandFactoryMethod:
    def short_help_message(self):
        raise NotImplementedError

    def build(self, args: List[str], settings: Settings) -> Command:
        raise NotImplementedError
