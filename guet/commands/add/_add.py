from typing import List

from guet.commands import CommandFactory
from guet.committers import Committers2
from guet.files import FileSystem
from guet.git import Git
from guet.steps import Step, IfStep
from guet.steps.check import VersionCheck, HelpCheck, GitRequiredCheck
from guet.steps.preparation import InitializePreparation

from ._args import ArgumentCheck
from ._add_committer import AddCommitter
from ._local_file_initialization import LocalFilesInitialization
from ._overwrite import OverwritingCommitterCheck


class AddCommandFactory(CommandFactory):
    def __init__(self, file_system: FileSystem, committers: Committers2, git: Git):
        self.file_system = file_system
        self.committers = committers
        self.git = git

    def choose(self, args: List[str]):
        return 1 if '--local' in args else 0

    def build(self) -> Step:
        return VersionCheck() \
            .next(HelpCheck('temp')) \
            .next(InitializePreparation(self.file_system)) \
            .next(ArgumentCheck()) \
            .next(IfStep(lambda args: '--local' in args,
                         GitRequiredCheck(self.git)
                         .next(LocalFilesInitialization(self.file_system, self.committers)))) \
            .next(OverwritingCommitterCheck(self.committers)) \
            .next(AddCommitter(self.committers))
