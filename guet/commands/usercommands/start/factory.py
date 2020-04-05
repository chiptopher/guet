from typing import List

from guet.commands.command import Command
from guet.commands.usercommands.help.help_message_builder import HelpMessageBuilder, FlagBuilder, FlagsBuilder
from guet.commands.usercommands.start.create_alongside_hook_strategy import CreateAlongsideHookStrategy
from guet.commands.usercommands.start.create_hook_strategy import CreateHookStrategy
from guet.commands.usercommands.start.start_strategy import PromptUserForHookTypeStrategy
from guet.commands.strategies.strategy_command import StrategyCommand
from guet.commands.usercommands.usercommand_factory import UserCommandFactory
from guet.git.git import Git
from guet.git.git_path_from_cwd import git_path_from_cwd
from guet.settings.settings import Settings

START_HELP_MESSAGE = HelpMessageBuilder('guet start',
                                        'Initialize current .git project to use guet.') \
    .flags(FlagsBuilder([FlagBuilder('-a/--alongside', 'Create hooks alongside current hooks with "-guet" on the end'),
                         FlagBuilder('-o/--overwrite', 'Overwrite current hooks')])).build()


class StartCommandFactory(UserCommandFactory):
    def short_help_message(self) -> str:
        return 'Start guet usage in the repository at current directory'

    def build(self, args: List[str], settings: Settings) -> Command:
        git_path = git_path_from_cwd().replace('/hooks', '')
        git = Git(git_path)
        if '-a' in args or '--alongside' in args:
            strategy = CreateAlongsideHookStrategy(git_path, self.context)
        elif '-o' in args or '--overwrite' in args:
            strategy = CreateHookStrategy(git_path, self.context)
        elif git.non_guet_hooks_present():
            strategy = PromptUserForHookTypeStrategy(git_path, self.context)
        else:
            strategy = CreateHookStrategy(git_path, self.context)
        return StrategyCommand(strategy)
