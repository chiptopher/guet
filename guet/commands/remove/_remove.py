from guet.commands import CommandFactory
from guet.steps import Step
from guet.steps.check import CommittersExistCheck, HelpCheck, VersionCheck
from guet.steps.preparation import InitializePreparation
from guet.util import HelpMessageBuilder

from ._remove_committer import RemoveCommitterAction

REMOVE_HELP_MESSAGE = HelpMessageBuilder('guet remove <initials>',
                                         ('Remove committer '
                                          'with given initials from system.')).build()


class RemoveCommandFactory(CommandFactory):
    def __init__(self, file_system, committers):
        self.committers = committers
        self.file_system = file_system

    def build(self) -> Step:
        return VersionCheck() \
            .next(HelpCheck(REMOVE_HELP_MESSAGE, stop_on_no_args=True)) \
            .next(InitializePreparation(self.file_system)) \
            .next(CommittersExistCheck(self.committers)) \
            .next(RemoveCommitterAction(self.committers))
