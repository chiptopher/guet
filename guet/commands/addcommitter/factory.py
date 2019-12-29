from typing import List

from guet.commands.command import Command
from guet.settings.settings import Settings
from guet.commands.command_factory import CommandFactoryMethod
from guet.commands.strategy_command import StrategyCommand
from guet.commands.too_few_args import TooFewArgsStrategy
from guet.commands.argsettingcommand import ArgSettingCommand
from guet.commands.strategy import CommandStrategy
from guet.commands.too_many_args import TooManyArgsStrategy
from guet.commands.addcommitter.add_committer_strategy import AddCommitterStrategy
from guet.commands.help_message_strategy import HelpMessageStrategy


class AddCommitterFactory(CommandFactoryMethod):
    _HELP = 'usage: guet add <initials> <"name"> <email>'

    def build(self, args: List[str], settings: Settings) -> Command:
        strategy = self._choose_strategy(args[1:], settings)
        return StrategyCommand(strategy)

    def short_help_message(self):
        return 'Add committer to the list of available committers'

    def _choose_strategy(self, args: List[str], _: Settings) -> CommandStrategy:
        if len(args) == 0:
            return HelpMessageStrategy(self._HELP)
        if len(args) < 3:
            return TooFewArgsStrategy(self._HELP)
        elif len(args) > 3:
            return TooManyArgsStrategy()
        else:
            return AddCommitterStrategy(args[0], args[1], args[2])
