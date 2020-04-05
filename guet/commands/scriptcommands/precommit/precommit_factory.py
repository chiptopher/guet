from typing import List

from guet.commands.command import Command
from guet.commands.command_factory import CommandFactoryMethod
from guet.commands.scriptcommands.precommit.precommit_strategy import PreCommitStrategy
from guet.commands.strategies.error_strategy import ErrorStrategy
from guet.commands.strategies.strategy_command import StrategyCommand
from guet.settings.settings import Settings

NO_COMMITTERS_SET_ERROR_MESSAGE = 'You must set your pairs before you can commit.\n'


class PreCommitFactory(CommandFactoryMethod):
    def build(self, args: List[str], settings: Settings) -> Command:
        if len(self.context.committers.current()) > 0:
            return StrategyCommand(PreCommitStrategy())
        else:
            return StrategyCommand(ErrorStrategy(NO_COMMITTERS_SET_ERROR_MESSAGE))
