from typing import List

from guet.commands.command import Command
from guet.commands.command_factory_decorator import CommandFactoryDecorator
from guet.commands.do_nothing_strategy import DoNothingStrategy
from guet.commands.strategy_command import StrategyCommand
from guet.config.already_initialized import already_initialized
from guet.settings.settings import Settings

INIT_REQUIRED_ERROR_MESSAGE = ('guet has not been initialized yet! ' +
                               'Please do so by running the command "guet init".')


class InitRequiredDecorator(CommandFactoryDecorator):
    def build(self, args: List[str], settings: Settings) -> Command:
        if already_initialized():
            return self.decorated.build(args, settings)
        else:
            print(INIT_REQUIRED_ERROR_MESSAGE)
            exit(1)
            return StrategyCommand(DoNothingStrategy())
