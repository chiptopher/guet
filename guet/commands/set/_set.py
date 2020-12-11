from guet.commands import CommandFactory
from guet.steps import Step
from guet.steps.check import VersionCheck, HelpCheck, GitRequiredCheck
from guet.steps.preparation import InitializePreparation
from guet.util import HelpMessageBuilder

from ._committers_exist import CommittersExistCheck
from ._set_committers import SetCommittersAction


SET_HELP_MESSAGE = HelpMessageBuilder(
    'guet set <initials> [<initials> ...]', 'Get current committers.').build()


class SetCommittersCommand(CommandFactory):
    def __init__(self, file_system, committers, context, git):
        self.file_system = file_system
        self.committers = committers
        self.context = context
        self.git = git

    def build(self) -> Step:
        return VersionCheck() \
            .next(HelpCheck(SET_HELP_MESSAGE, stop_on_no_args=True)) \
            .next(InitializePreparation(self.file_system)) \
            .next(GitRequiredCheck(self.git)) \
            .next(CommittersExistCheck(self.committers)) \
            .next(SetCommittersAction(self.committers, self.context))
