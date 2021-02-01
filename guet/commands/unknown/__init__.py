from guet.commands import CommandFactory, CommandMap
from guet.files import FileSystem
from guet.steps import Step
from guet.steps.check import VersionCheck

from ._usage import UsageAction


class UnknownCommandFactory(CommandFactory):
    def __init__(self, command_map: CommandMap, file_system: FileSystem):
        self.command_map = command_map

    def build(self) -> Step:
        return VersionCheck() \
            .next(UsageAction(self.command_map))
