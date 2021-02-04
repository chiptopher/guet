from typing import List

from guet.commands import CommandFactory
from guet.committers.committers import Committers
from guet.files import FileSystem
from guet.steps import OptionStep, Step
from guet.steps.check import VersionCheck, HelpCheck
from guet.steps.preparation import InitializePreparation

from ._args import ArgumentCheck
from ._global_add import AddCommittersGlobally
from ._local_add import AddCommittersLocally
from ._local_file_initialization import LocalFilesInitialization
from ._overwrite import OverwritingCommitterCheck


class AddCommandFactory(CommandFactory):
    def __init__(self, file_system: FileSystem, committers: Committers):
        self.file_system = file_system
        self.committers = committers

    def choose(self, args: List[str]):
        return 1 if '--local' in args else 0

    def build(self) -> Step:
        return VersionCheck() \
            .next(HelpCheck('temp')) \
            .next(InitializePreparation(self.file_system)) \
            .next(OverwritingCommitterCheck(self.committers)) \
            .next(OptionStep(
                [
                    self._global_add_steps(),
                    self._local_add_steps()
                ],
                self.choose
            )) \


    def _global_add_steps(self) -> Step:
        return ArgumentCheck() \
            .next(AddCommittersGlobally(self.committers))

    def _local_add_steps(self) -> Step:
        return ArgumentCheck() \
            .next(LocalFilesInitialization(self.file_system)) \
            .next(AddCommittersLocally(self.committers))
