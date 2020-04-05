from typing import List

from guet.commands.command import Command
from guet.commands.command_factory import CommandFactoryMethod
from guet.commands.scriptcommands.commitmsg.commitmsg_strategy import CommitMsgStrategy
from guet.commands.strategies.strategy_command import StrategyCommand
from guet.settings.settings import Settings


class CommitMsgFactory(CommandFactoryMethod):
    def build(self, args: List[str], settings: Settings) -> Command:
        return StrategyCommand(CommitMsgStrategy(self.context))
