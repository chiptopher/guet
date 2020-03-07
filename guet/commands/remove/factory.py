from typing import List

from guet.commands.command import Command
from guet.commands.command_factory import CommandFactoryMethod
from guet.commands.help.help_message_builder import HelpMessageBuilder
from guet.commands.remove.remove_strategy import RemoveCommitterStrategy
from guet.commands.strategy_command import StrategyCommand
from guet.settings.settings import Settings

REMOVE_HELP_MESSAGE = HelpMessageBuilder('guet remove <initials>', ('Remove committer '
                                                                    'with given initials from system.')).build()


class RemoveCommandFactory(CommandFactoryMethod):

    def short_help_message(self) -> str:
        return 'Removes committer'

    def build(self, args: List[str], settings: Settings) -> Command:
        return StrategyCommand(RemoveCommitterStrategy(args[1], self.context))
