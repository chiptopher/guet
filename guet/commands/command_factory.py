from typing import List

from guet.settings.settings import Settings
from guet.commands.argsettingcommand import ArgSettingCommand


class CommandFactoryMethod:
    def short_help_message(self) -> str:
        raise NotImplementedError

    def build(self, args: List[str], settings: Settings) -> ArgSettingCommand:
        raise NotImplementedError
