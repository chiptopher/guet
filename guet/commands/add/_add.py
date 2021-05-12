from typing import List

from guet.commands import CommandFactory
from guet.committers import Committers2
from guet.files import FileSystem
from guet.git import Git
from guet.steps import IfStep, Step
from guet.steps.check import GitRequiredCheck, HelpCheck, VersionCheck
from guet.steps.preparation import InitializePreparation
from guet.util import FlagBuilder, FlagsBuilder, HelpMessageBuilder

from ._add_committer import AddCommitter
from ._args import ArgumentCheck
from ._local_file_initialization import LocalFilesInitialization
from ._overwrite import OverwritingCommitterCheck

_HELP_MESSAGE = HelpMessageBuilder('guet add <initials> <"name"> <email>',
                                   'Add committer to make available for commit tracking.') \
    .flags(FlagsBuilder([FlagBuilder('--local', 'Save the committer locally')])).build()

class AddCommandFactory(CommandFactory):
    def __init__(self, file_system: FileSystem, committers: Committers2, git: Git):
        self.file_system = file_system
        self.committers = committers
        self.git = git

    def choose(self, args: List[str]):
        return 1 if '--local' in args else 0

    def build(self) -> Step:
        return VersionCheck() \
            .next(HelpCheck(_HELP_MESSAGE)) \
            .next(InitializePreparation(self.file_system)) \
            .next(ArgumentCheck()) \
            .next(IfStep(lambda args: '--local' in args,
                         GitRequiredCheck(self.git)
                         .next(LocalFilesInitialization(self.file_system, self.committers)))) \
            .next(OverwritingCommitterCheck(self.committers)) \
            .next(AddCommitter(self.committers))
