from typing import List

from guet.commands.command_factory import CommandFactoryMethod
from guet.commands.setcommitters.set_committers_strategy import SetCommittersStrategy
from guet.commands.strategy_command import StrategyCommand
from guet.settings.settings import Settings

SET_HELP_MESSAGE = 'usage: guet set <initials> [<initials> ...]'


class SetCommittersCommandFactory(CommandFactoryMethod):
    def build(self, args: List[str], settings: Settings):
        return StrategyCommand(SetCommittersStrategy(args[1:]))

    def short_help_message(self):
        return 'Set the current committers'
