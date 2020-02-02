from typing import List

from guet.commands.cancellable_strategy import CancelableCommandStrategy
from guet.commands.command import Command
from guet.commands.do_nothing_strategy import DoNothingStrategy
from guet.commands.help.help_message_builder import HelpMessageBuilder
from guet.config.get_committers import get_committers
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

    def _initials_already_present(self, initials):
        return len([committer for committer in get_committers() if committer.initials == initials]) != 0

    def _prompt(self, new_initials: str, new_name: str, new_email: str) -> str:
        matching_committer = next((committer for committer in get_committers() if committer.initials == new_initials))
        warning = (f'Matching initials "{new_initials}". Adding "{new_name}" <{new_email}> '
                   f'will overwrite "{matching_committer.name}" <{matching_committer.email}>. Would you '
                   f'like to continue (y) or cancel (x)?')
        return warning

    def _choose_strategy(self, args: List[str], _: Settings) -> CommandStrategy:
        if len(args) < 3:
            return TooFewArgsStrategy(ADD_COMMITTER_HELP_MESSAGE)
        elif len(args) > 3:
            return TooManyArgsStrategy()
        else:
            initials, name, email = args
            add_committers_strategy = AddCommitterStrategy(initials, name, email)
            if self._initials_already_present(initials):
                return CancelableCommandStrategy(self._prompt(initials, name, email),
                                                 add_committers_strategy,
                                                 DoNothingStrategy())
            else:
                return add_committers_strategy
