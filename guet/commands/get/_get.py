from guet.commands import CommandFactory
from guet.committers.committers import Committers
from guet.files import FileSystem
from guet.steps import Step
from guet.steps.check import HelpCheck, VersionCheck
from guet.steps.preparation import InitializePreparation
from guet.util import FlagBuilder, FlagsBuilder, HelpMessageBuilder

from ._action import GetCommittersAction

GET_HELP_MESSAGE = HelpMessageBuilder('guet get <identifier> [-flag, ...]',
                                      'Get currently set information.') \
    .explanation('Valid Identifier\n\tcurrent - lists currently set committers\n\tcommitters - lists all committers') \
    .build()


class GetCommandFactory(CommandFactory):
    def __init__(self, file_system: FileSystem, committers: Committers):
        self.file_system = file_system
        self.committers = committers

    def build(self) -> Step:
        return VersionCheck() \
            .next(HelpCheck(GET_HELP_MESSAGE)) \
            .next(InitializePreparation(self.file_system)) \
            .next(GetCommittersAction(self.committers))
