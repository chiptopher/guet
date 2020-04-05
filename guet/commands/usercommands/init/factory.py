from typing import List

from guet.commands.command import Command
from guet.commands.strategies.lambda_strategy import LambdaStrategy
from guet.commands.strategies.print_strategy import PrintCommandStrategy
from guet.commands.strategies.strategy_command import StrategyCommand
from guet.commands.usercommands.help.help_message_builder import HelpMessageBuilder
from guet.commands.usercommands.usercommand_factory import UserCommandFactory
from guet.config.already_initialized import already_initialized
from guet.config.initialize import initialize
from guet.settings.settings import Settings

INIT_HELP_MESSAGE = HelpMessageBuilder('guet init', 'Initialized guet for use on this computer.').build()


class InitCommandFactory(UserCommandFactory):

    def short_help_message(self) -> str:
        return 'Initialize guet for use'

    def build(self, args: List[str], settings: Settings) -> Command:
        if not already_initialized():
            return StrategyCommand(LambdaStrategy(lambda: initialize()))
        else:
            return StrategyCommand(PrintCommandStrategy('Config folder already exists.'))
