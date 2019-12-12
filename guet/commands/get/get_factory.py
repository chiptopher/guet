from typing import List

from guet.commands.command import Command
from guet.commands.command_factory import CommandFactoryMethod
from guet.commands.get.all_committers_strategy import AllCommittersStrategy
from guet.commands.get.current_committers_strategy import CurrentCommittersStrategy
from guet.commands.get.full_committers_list_strategy import FullCommittersListStrategy
from guet.commands.get.get_command import GetCommand
from guet.commands.get.invalid_identifier_strategy import InvalidIdentifierStrategy
from guet.commands.get.short_list_strategy import ShortCommittersListStrategy
from guet.commands.strategy_command import StrategyCommand
from guet.config.get_committers import get_committers
from guet.config.get_current_committers import get_current_committers
from guet.settings.settings import Settings


class GetCommandFactory(CommandFactoryMethod):

    def short_help_message(self):
        pass

    def build(self, args: List[str], settings: Settings) -> Command:
        if len(args) > 1:
            identifier = args[1]
            list_flag = False
            if '-l' in args:
                list_flag = True
            if identifier == 'current':
                strategy = CurrentCommittersStrategy(FullCommittersListStrategy(get_current_committers()))
            elif identifier == 'committers':
                if list_flag:
                    strategy = AllCommittersStrategy(ShortCommittersListStrategy(get_committers()))
                else:
                    strategy = AllCommittersStrategy(FullCommittersListStrategy(get_committers()))
            else:
                strategy = InvalidIdentifierStrategy()
            return GetCommand(args, settings, strategy)
