from typing import List

from guet.commands.command import Command
from guet.commands.command_factory import CommandFactoryMethod
from guet.commands.command_factory_decorator import CommandFactoryDecorator
from guet.commands.help_message_strategy import HelpMessageStrategy
from guet.commands.strategy_command import StrategyCommand
from guet.settings.settings import Settings


class HelpDecorator(CommandFactoryDecorator):

    def __init__(self, decorated: CommandFactoryMethod, help_message: str):
        super().__init__(decorated)
        self._help_message = help_message

    def build(self, args: List[str], settings: Settings) -> Command:
        if len(args) is 1 or '-h' in args or '--help' in args:
            return StrategyCommand(HelpMessageStrategy(self._help_message))
        else:
            return self.decorated.build(args, settings)
