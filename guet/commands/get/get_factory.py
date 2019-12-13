from typing import List, Type

from guet.commands.command import Command
from guet.commands.command_factory import CommandFactoryMethod
from guet.commands.get.all_committers_strategy import AllCommittersStrategy
from guet.commands.get.current_committers_strategy import CurrentCommittersStrategy
from guet.commands.get.full_committers_list_strategy import FullCommittersListStrategy
from guet.commands.get.invalid_identifier_strategy import InvalidIdentifierStrategy
from guet.commands.get.short_list_strategy import ShortCommittersListStrategy
from guet.commands.help_message_strategy import HelpMessageStrategy
from guet.commands.strategy_command import StrategyCommand
from guet.config.get_committers import get_committers
from guet.config.get_current_committers import get_current_committers
from guet.settings.settings import Settings


class GetCommandFactory(CommandFactoryMethod):

    def short_help_message(self):
        pass

    def build(self, args: List[str], settings: Settings) -> Command:
        if len(args) > 1:
            printing_strategy_type = self._determine_printing_strategy(args)
            strategy = self._determine_identifier_strategy(args, printing_strategy_type)
            return StrategyCommand(args, settings, strategy)
        else:
            return StrategyCommand(args, settings, HelpMessageStrategy(
                """usage: guet get <identifier>\n\nValid Identifier\n\n\tcurrent - lists currently set committers\n\tcomitters - lists all committers"""))

    def _determine_printing_strategy(self, args: List[str]):
        if '-l' in args:
            return ShortCommittersListStrategy
        else:
            return FullCommittersListStrategy

    def _determine_identifier_strategy(self, args: List[str], printing_strategy_type):
        identifier = args[1]
        if identifier == 'current':
            strategy = CurrentCommittersStrategy(printing_strategy_type(get_current_committers()))
        elif identifier == 'committers':
            strategy = AllCommittersStrategy(printing_strategy_type(get_committers()))
        else:
            strategy = InvalidIdentifierStrategy()
        return strategy
