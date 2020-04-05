from typing import List

from guet.commands.command import Command
from guet.commands.decorators.command_factory_decorator import CommandFactoryDecorator
from guet.commands.strategies.print_strategy import PrintCommandStrategy
from guet.commands.strategies.strategy_command import StrategyCommand
from guet.settings.settings import Settings
import guet


class VersionDecorator(CommandFactoryDecorator):
    def build(self, args: List[str], settings: Settings) -> Command:
        if '-v' in args or '--version' in args:
            return StrategyCommand(PrintCommandStrategy(guet.__version__))
        else:
            return self.decorated.build(args, settings)
