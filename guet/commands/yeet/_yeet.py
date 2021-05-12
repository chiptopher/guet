from typing import List

from guet.commands import CommandFactory
from guet.files import FileSystem
from guet.git import Git
from guet.steps import Step
from guet.steps.check import GitRequiredCheck, HelpCheck, VersionCheck
from guet.steps.preparation import InitializePreparation
from guet.util import FlagBuilder, FlagsBuilder, HelpMessageBuilder

from ._remove_global import RemoveGlobal
from ._remove_local import RemoveLocal

_GLOBAL_EXPLANATION = 'Remove guet configuration from home directory'

_HELP_MESSAGE = HelpMessageBuilder('guet yeet',
                                   'Remove guet configuration.') \
    .flags(FlagsBuilder([FlagBuilder('-g/--global', _GLOBAL_EXPLANATION)])).build()


class YeetCommandFactory(CommandFactory):
    def __init__(self, file_system: FileSystem, git: Git):
        self.file_system = file_system
        self.git = git

    def choose(self, args: List[str]):
        return 1 if '--local' in args else 0

    def build(self) -> Step:
        return VersionCheck() \
            .next(HelpCheck(_HELP_MESSAGE)) \
            .next(InitializePreparation(self.file_system)) \
            .next(GitRequiredCheck(self.git)) \
            .next(RemoveLocal(self.git, self.file_system)) \
            .next(RemoveGlobal())
