from typing import List

from guet.commands.strategies.strategy_command import StrategyCommand
from guet.commands.usercommands.help.help_message_builder import HelpMessageBuilder
from guet.commands.usercommands.setcommitters.set_committers_strategy import SetCommittersStrategy
from guet.commands.usercommands.usercommand_factory import UserCommandFactory
from guet.settings.settings import Settings

SET_HELP_MESSAGE = HelpMessageBuilder('guet set <initials> [<initials> ...]', 'Get current committers.').build()


class SetCommittersCommandFactory(UserCommandFactory):
    def build(self, args: List[str], settings: Settings):
        return StrategyCommand(SetCommittersStrategy(args[1:], self.context))

    def short_help_message(self):
        return 'Set the current committers'
