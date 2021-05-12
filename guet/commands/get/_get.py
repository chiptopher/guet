from guet.commands import CommandFactory
from guet.committers import Committers2 as Committers
from guet.committers import CurrentCommitters
from guet.files import FileSystem
from guet.steps import Step
from guet.steps.check import HelpCheck, VersionCheck
from guet.steps.preparation import InitializePreparation, SwapToLocal
from guet.util import HelpMessageBuilder

from ._action import GetCommittersAction

GET_HELP_MESSAGE = HelpMessageBuilder('guet get <identifier> [-flag, ...]',
                                      'Get currently set information.') \
    .explanation(('Valid Identifier\n\tcurrent - lists currently set committers'
                  '\n\tall - lists all committers')) \
    .build()


class GetCommandFactory(CommandFactory):
    def __init__(self,
                 file_system: FileSystem,
                 committers: Committers,
                 current_committers: CurrentCommitters):

        self.file_system = file_system
        self.committers = committers
        self.current = current_committers

    def build(self) -> Step:
        return VersionCheck() \
            .next(HelpCheck(GET_HELP_MESSAGE, stop_on_no_args=True)) \
            .next(InitializePreparation(self.file_system)) \
            .next(SwapToLocal(self.committers)) \
            .next(GetCommittersAction(self.committers, self.current))
