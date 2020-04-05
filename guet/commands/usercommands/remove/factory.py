from typing import List

from guet.commands.command import Command
from guet.commands.strategies.strategy_command import StrategyCommand
from guet.commands.usercommands.help.help_message_builder import HelpMessageBuilder
from guet.commands.usercommands.remove.remove_strategy import RemoveCommitterStrategy
from guet.commands.usercommands.usercommand_factory import UserCommandFactory
from guet.settings.settings import Settings

REMOVE_HELP_MESSAGE = HelpMessageBuilder('guet remove <initials>', ('Remove committer '
                                                                    'with given initials from system.')).build()


class RemoveCommandFactory(UserCommandFactory):

    def short_help_message(self) -> str:
        return 'Removes committer'

    def build(self, args: List[str], settings: Settings) -> Command:
        return StrategyCommand(RemoveCommitterStrategy(args[1], self.context))
