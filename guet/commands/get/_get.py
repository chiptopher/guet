from guet.commands import CommandFactory
from guet.committers.committers import Committers
from guet.files import FileSystem
from guet.steps import Step
from guet.steps.check import VersionCheck, HelpCheck
from guet.steps.preparation import InitializePreparation

from ._action import GetCommittersAction


class GetCommandFactory(CommandFactory):
    def __init__(self, file_system: FileSystem, committers: Committers):
        self.file_system = file_system
        self.committers = committers

    def build(self) -> Step:
        return VersionCheck() \
            .next(HelpCheck('temp')) \
            .next(InitializePreparation(self.file_system)) \
            .next(GetCommittersAction(self.committers))