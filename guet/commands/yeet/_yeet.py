from typing import List

from guet.commands import CommandFactory
from guet.files import FileSystem
from guet.git import Git
from guet.steps import Step
from guet.steps.check import GitRequiredCheck, HelpCheck, VersionCheck
from guet.steps.preparation import InitializePreparation

from ._remove_global import RemoveGlobal
from ._remove_local import RemoveLocal


class YeetCommandFactory(CommandFactory):
    def __init__(self, file_system: FileSystem, git: Git):
        self.file_system = file_system
        self.git = git

    def choose(self, args: List[str]):
        return 1 if '--local' in args else 0

    def build(self) -> Step:
        return VersionCheck() \
            .next(HelpCheck('temp')) \
            .next(InitializePreparation(self.file_system)) \
            .next(GitRequiredCheck(self.git)) \
            .next(RemoveLocal()) \
            .next(RemoveGlobal())
