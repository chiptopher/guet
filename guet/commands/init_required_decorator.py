from typing import List

from guet.commands.command import Command
from guet.commands.command_factory_decorator import CommandFactoryDecorator
from guet.config.already_initialized import already_initialized
from guet.settings.settings import Settings


class InitRequiredDecorator(CommandFactoryDecorator):
    def build(self, args: List[str], settings: Settings) -> Command:
        if already_initialized():
            return self.decorated.build(args, settings)
        else:
            print(('guet has not been initialized yet! ' +
                   'Please do so by running the command "guet init".'))
            exit(1)
