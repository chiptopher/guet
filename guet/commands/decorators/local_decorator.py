from typing import List

from guet.commands.command import Command
from guet.commands.decorators.command_factory_decorator import CommandFactoryDecorator
from guet.commands.decorators.start_required_decorator import StartRequiredDecorator
from guet.settings.settings import Settings


class LocalDecorator(CommandFactoryDecorator):

    def build(self, args: List[str], settings: Settings) -> Command:
        if '--local' in args:
            return StartRequiredDecorator(self.decorated).build(args, settings)
        else:
            return self.decorated.build(args, settings)
