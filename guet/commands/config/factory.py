from typing import List

from guet.settings.settings import Settings
from guet.commands.command_factory import CommandFactoryMethod
from guet.commands.config.command import ConfigSetCommand


class ConfigCommandFactory(CommandFactoryMethod):
    def short_help_message(self):
        return 'Change setting values'

    def build(self, args: List[str], settings: Settings):
        return ConfigSetCommand(args, settings)
