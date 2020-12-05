from guet.commands import CommandFactory, CommandMap
from guet.files import FileSystem
from guet.steps import Step
from guet.steps.check import VersionCheck
from guet.steps.preparation import InitializePreparation

from ._usage import UsageAction


class HelpCommandFactory(CommandFactory):
    def __init__(self, command_map: CommandMap, file_system: FileSystem):
        self.command_map = command_map
        self.file_system = file_system

    def build(self) -> Step:
        return VersionCheck() \
            .next(InitializePreparation(self.file_system)) \
            .next(UsageAction(self.command_map))
