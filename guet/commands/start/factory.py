from typing import List

from guet.commands.command import Command
from guet.commands.command_factory import CommandFactoryMethod
from guet.commands.start.start_strategy import StartCommandStrategy
from guet.commands.strategy_command import StrategyCommand
from guet.settings.settings import Settings


class StartCommandFactory(CommandFactoryMethod):
    def short_help_message(self) -> str:
        return 'Start guet usage in the repository at current directory'

    def build(self, args: List[str], settings: Settings) -> Command:
        return StrategyCommand(args, settings, StartCommandStrategy())
