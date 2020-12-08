from guet.commands import CommandFactory
from guet.steps import Step
from guet.steps.check import VersionCheck, HelpCheck
from guet.steps.preparation import InitializePreparation

from ._committers_exist import CommittersExistCheck
from ._set_committers import SetCommittersAction


class SetCommittersCommand(CommandFactory):
    def __init__(self, file_system, committers, context):
        self.file_system = file_system
        self.committers = committers
        self.context = context

    def build(self) -> Step:
        return VersionCheck() \
            .next(HelpCheck('temp')) \
            .next(InitializePreparation(self.file_system)) \
            .next(CommittersExistCheck(self.committers)) \
            .next(SetCommittersAction(self.committers, self.context))
