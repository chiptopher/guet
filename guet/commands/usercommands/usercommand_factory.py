from typing import List

from guet.commands.command import Command
from guet.commands.command_factory import CommandFactoryMethod
from guet.settings.settings import Settings


class UserCommandFactory(CommandFactoryMethod):
    def build(self, args: List[str], settings: Settings) -> Command:
        raise NotImplementedError

    def short_help_message(self) -> str:
        raise NotImplementedError
