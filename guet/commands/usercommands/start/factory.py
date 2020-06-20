from typing import List

from guet.commands.command import Command
from guet.commands.usercommands.help.help_message_builder import HelpMessageBuilder, FlagBuilder, FlagsBuilder
from guet.commands.usercommands.start._create_alongside_hook_strategy import CreateAlongsideHookAction
from guet.commands.usercommands.start._create_hook_strategy import CreateHookAction
from guet.commands.usercommands.start._start_strategy import PromptUserForHookTypeAction
from guet.commands.strategies.strategy_command import StrategyCommand
from guet.commands.usercommands.usercommand_factory import UserCommandFactory
from guet.settings.settings import Settings

START_HELP_MESSAGE = HelpMessageBuilder('guet start',
                                        'Initialize current .git project to use guet.') \
    .flags(FlagsBuilder([FlagBuilder('-a/--alongside', 'Create hooks alongside current hooks with "-guet" on the end'),
                         FlagBuilder('-o/--overwrite', 'Overwrite current hooks')])).build()


class StartCommandFactory(UserCommandFactory):
    def short_help_message(self) -> str:
        return 'Start guet usage in the repository at current directory'

    def build(self, args: List[str], settings: Settings) -> Command:
        git = self.context.git
        if '-a' in args or '--alongside' in args:
            hook_action = CreateAlongsideHookAction(git)
        elif '-o' in args or '--overwrite' in args:
            hook_action = CreateHookAction(git)
        elif git.non_guet_hooks_present():
            hook_action = PromptUserForHookTypeAction(git)
        else:
            hook_action = CreateHookAction(git)
        return StrategyCommand(hook_action)
