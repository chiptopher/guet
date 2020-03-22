from os import getcwd
from typing import List

from guet.commands.addcommitter.add_committer_locally_strategy import AddCommitterLocallyStrategy
from guet.commands.addcommitter.add_committer_strategy import AddCommitterGloballyStrategy
from guet.commands.cancellable_strategy import CancelableCommandStrategy
from guet.commands.command import Command
from guet.commands.command_factory import CommandFactoryMethod
from guet.commands.do_nothing_strategy import DoNothingStrategy
from guet.commands.help.help_message_builder import HelpMessageBuilder, FlagsBuilder, FlagBuilder
from guet.commands.strategy import CommandStrategy
from guet.commands.strategy_command import StrategyCommand
from guet.commands.too_few_args import TooFewArgsStrategy
from guet.commands.too_many_args import TooManyArgsStrategy
from guet.config.committer import Committer
from guet.settings.settings import Settings

ADD_COMMITTER_HELP_MESSAGE = HelpMessageBuilder('guet add <initials> <"name"> <email>',
                                                "Add committer to make available for commit tracking.") \
    .flags(FlagsBuilder([FlagBuilder('--local', 'Save the committer locally')])).build()


def _should_add_local(args):
    return '--local' in args


def _args_without_local_flag(args):
    return [arg for arg in args if arg != '--local']


class AddCommitterFactory(CommandFactoryMethod):
    def build(self, args: List[str], settings: Settings) -> Command:
        strategy = self._choose_strategy(args[1:], settings)
        return StrategyCommand(strategy)

    def short_help_message(self):
        return 'Add committer to the list of available committers'

    def _commiter_with_matching_initials(self, initials) -> Committer:
        try:
            return next(committer for committer in self.context.committers.all() if committer.initials == initials)
        except StopIteration:
            return None

    def _prompt(self, new_initials: str, new_name: str, new_email: str) -> str:
        matching_committer = next(
            (committer for committer in self.context.committers.all() if committer.initials == new_initials))
        warning = (f'Matching initials "{new_initials}". Adding "{new_name}" <{new_email}> '
                   f'will overwrite "{matching_committer.name}" <{matching_committer.email}>. Would you '
                   f'like to continue (y) or cancel (x)?')
        return warning

    def _choose_strategy(self, args: List[str], _: Settings) -> CommandStrategy:
        if len(_args_without_local_flag(args)) < 3:
            return TooFewArgsStrategy(ADD_COMMITTER_HELP_MESSAGE)
        elif len(_args_without_local_flag(args)) > 3:
            return TooManyArgsStrategy()
        else:
            return self._choose_creation_strategy(args)

    def _choose_creation_strategy(self, args):
        initials, name, email = _args_without_local_flag(args)
        found = self._commiter_with_matching_initials(initials)
        if _should_add_local(args):
            if found:
                print((f'Adding committer with initials "{initials}" shadows the '
                       f'global committer "{found.initials}" - "{found.name}" <{found.email}>'))
            add_committers_strategy = AddCommitterLocallyStrategy(initials, name, email,
                                                                  project_root=getcwd(),
                                                                  committers=self.context.committers)
        else:
            add_committers_strategy = AddCommitterGloballyStrategy(initials, name, email, self.context.committers)
        if found and not _should_add_local(args):
            return CancelableCommandStrategy(self._prompt(initials, name, email),
                                             add_committers_strategy,
                                             DoNothingStrategy())
        else:
            return add_committers_strategy
