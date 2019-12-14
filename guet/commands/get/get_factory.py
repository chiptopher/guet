from typing import List, Type

from guet.commands.command import Command
from guet.commands.command_factory import CommandFactoryMethod
from guet.commands.get.committer_printing_strategy import CommitterPrintingStrategy
from guet.commands.get.invalid_identifier_strategy import InvalidIdentifierStrategy
from guet.commands.help_message_strategy import HelpMessageStrategy
from guet.commands.strategy_command import StrategyCommand, CommandStrategy
from guet.config.committer import Committer
from guet.config.get_committers import get_committers
from guet.config.get_current_committers import get_current_committers
from guet.settings.settings import Settings


def print_full_names(committers: List[Committer]) -> None:
    for committer in committers:
        print(committer.pretty())


def print_only_initials(committers: List[Committer]) -> None:
    print(', '.join([committer.initials for committer in committers]))


class GetCommandFactory(CommandFactoryMethod):

    def short_help_message(self):
        pass

    def build(self, args: List[str], settings: Settings) -> Command:
        if len(args) > 1:
            try:
                strategy = self._determine_strategy(args)
                return StrategyCommand(args, settings, strategy)
            except AttributeError:
                return StrategyCommand(args, settings, InvalidIdentifierStrategy())
        else:
            return StrategyCommand(args, settings, HelpMessageStrategy(
                """usage: guet get <identifier>\n\nValid Identifier\n\n\tcurrent - lists currently set committers\n\tcomitters - lists all committers"""))

    def _determine_identifier(self, identifier: str):
        if identifier == 'committers':
            return get_committers(), lambda: print('All committers')
        elif identifier == 'current':
            return get_current_committers(), lambda: print('Currently set committers')
        raise AttributeError

    def _determine_strategy(self, args: List[str]) -> CommandStrategy:
        identifier = args[1]
        committers, pre_print = self._determine_identifier(identifier)
        if '-l' in args:
            return CommitterPrintingStrategy(committers, lambda: None, print_only_initials)
        else:
            return CommitterPrintingStrategy(committers, pre_print, print_full_names)
