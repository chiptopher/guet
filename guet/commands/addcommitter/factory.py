from typing import List

from guet.commands.command import Command
from guet.commands.help.help_message_builder import HelpMessageBuilder
from guet.settings.settings import Settings
from guet.commands.command_factory import CommandFactoryMethod
from guet.commands.strategy_command import StrategyCommand
from guet.commands.too_few_args import TooFewArgsStrategy
from guet.commands.strategy import CommandStrategy
from guet.commands.too_many_args import TooManyArgsStrategy
from guet.commands.addcommitter.add_committer_strategy import AddCommitterStrategy

ADD_COMMITTER_HELP_MESSAGE = HelpMessageBuilder('guet add <initials> <"name"> <email>',
                                                "Add committer to make available for commit tracking.").build()


class AddCommitterFactory(CommandFactoryMethod):

    def build(self, args: List[str], settings: Settings) -> Command:
        strategy = self._choose_strategy(args[1:], settings)
        return StrategyCommand(strategy)

    def short_help_message(self):
        return 'Add committer to the list of available committers'

    def _choose_strategy(self, args: List[str], _: Settings) -> CommandStrategy:
        if len(args) < 3:
            return TooFewArgsStrategy(ADD_COMMITTER_HELP_MESSAGE)
        elif len(args) > 3:
            return TooManyArgsStrategy()
        else:
            return AddCommitterStrategy(args[0], args[1], args[2])
