from typing import List

from guet.commands import CommandFactory
from guet.files import FileSystem
from guet.git import Git
from guet.steps import OptionStep, Step
from guet.steps.action import PrintAction
from guet.steps.check import GitRequiredCheck, HelpCheck, VersionCheck
from guet.steps.preparation import InitializePreparation
from guet.util import FlagBuilder, FlagsBuilder, HelpMessageBuilder

from ._cancel_create_hook import CancelCreateHooks
from ._change_hooks_folder import ChangeHooksFolder
from ._create_hooks_alongside import CreateHooksAlongside
from ._create_hooks_normally import CreateHooksNormally

ALONGSIDE_FLAG_EXPLANATION = 'Create hooks alongside current hooks with "-guet" on the end'
SHORT_EXPLANATION = 'Initialize current .git project to use guet.'
START_HELP_MESSAGE = HelpMessageBuilder('guet start', SHORT_EXPLANATION) \
    .flags(FlagsBuilder([FlagBuilder('-a/--alongside', ALONGSIDE_FLAG_EXPLANATION),
                         FlagBuilder('-o/--overwrite', 'Overwrite current hooks'),
                         FlagBuilder('--location', 'Specify location to create hooks in')])).build()


def choose(args: List[str]):
    if '-a' in args or '--alongside' in args:
        return 1
    elif '-o' in args or '--overwrite' in args:
        return 0

    else:
        return 0


class InitCommandFactory(CommandFactory):
    def __init__(self, git: Git, file_system: FileSystem):
        self.git = git
        self.file_system = file_system

    def choose(self, args: List[str]):
        res = 0
        if '-a' in args or '--alongside' in args:
            res = 1
        elif '-o' in args or '--overwrite' in args:
            res = 0
        elif self.git.non_guet_hooks_present():
            res = self._capture_overwrite()
        else:
            res = 0
        return res

    def _capture_overwrite(self):
        print('There is already commit hooks in this project. You can')
        print('  (o) overwrite current hooks. This will delete any'
              ' matching hooks.')
        print(('  (a) create guet hooks alongside current ones.'
               'This will create them with \'-guet\' appended on'
               ' the name of the hook file.'))
        print('  (x) cancel the request. This will do nothing.')
        val = input()
        if val == 'o':
            return 0
        elif val == 'a':
            return 1
        else:
            return 2

    def build(self) -> Step:
        return VersionCheck() \
            .next(HelpCheck(START_HELP_MESSAGE)) \
            .next(InitializePreparation(self.file_system)) \
            .next(GitRequiredCheck(self.git)) \
            .next(ChangeHooksFolder(self.git)) \
            .next(OptionStep(
                [
                    CreateHooksNormally(self.git)
                    .next(PrintAction('guet successfully started in this repository.')),
                    CreateHooksAlongside(self.git)
                    .next(PrintAction('guet successfully started in this repository.')),
                    CancelCreateHooks()
                ],
                self.choose
            ))
