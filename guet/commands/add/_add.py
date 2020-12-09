from guet.commands import CommandFactory
from guet.committers.committers import Committers
from guet.files import FileSystem
from guet.steps import Step
from guet.steps.check import VersionCheck, HelpCheck
from guet.steps.preparation import InitializePreparation

from ._args import ArgumentCheck
from ._global_add import AddCommittersGlobally
from ._overwrite import OverwritingCommitterCheck


class AddCommandFactory(CommandFactory):
    def __init__(self, file_system: FileSystem, committers: Committers):
        self.file_system = file_system
        self.committers = committers

    def build(self) -> Step:
        return VersionCheck() \
            .next(HelpCheck('temp')) \
            .next(InitializePreparation(self.file_system)) \
            .next(ArgumentCheck()) \
            .next(OverwritingCommitterCheck(self.committers)) \
            .next(AddCommittersGlobally(self.committers))
