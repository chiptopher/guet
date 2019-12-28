from typing import List

from guet.commands.command import Command
from guet.commands.command_factory import CommandFactoryMethod
from guet.commands.lambda_strategy import LambdaStrategy
from guet.commands.print_strategy import PrintCommandStrategy
from guet.commands.strategy_command import StrategyCommand
from guet.config.already_initialized import already_initialized
from guet.config.initialize import initialize
from guet.settings.settings import Settings


class InitCommandFactory(CommandFactoryMethod):

    def short_help_message(self) -> str:
        return 'Initialize guet for use'

    def build(self, args: List[str], settings: Settings) -> Command:
        if not already_initialized():
            return StrategyCommand(args, settings, LambdaStrategy(lambda: initialize()))
        else:
            return StrategyCommand(args, settings, PrintCommandStrategy('Config folder already exists.'))
