from typing import List

from guet.commands.command import Command
from guet.commands.command_factory import CommandFactoryMethod
from guet.commands.help.help_message_builder import HelpMessageBuilder, FlagBuilder, FlagsBuilder
from guet.commands.start.create_alongside_hook_strategy import CreateAlongsideHookStrategy
from guet.commands.start.create_hook_strategy import CreateHookStrategy
from guet.commands.start.start_strategy import PromptUserForHookTypeStrategy
from guet.commands.strategy_command import StrategyCommand
from guet.git.git import Git
from guet.git.git_path_from_cwd import git_path_from_cwd
from guet.settings.settings import Settings

START_HELP_MESSAGE = HelpMessageBuilder('guet start',
                                        'Initialize current .git project to use guet.') \
    .flags(FlagsBuilder([FlagBuilder('-a/--alongside', 'Create hooks alongside current hooks with "-guet" on the end'),
                         FlagBuilder('-o/--overwrite', 'Overwrite current hooks')])).build()


class StartCommandFactory(CommandFactoryMethod):
    def short_help_message(self) -> str:
        return 'Start guet usage in the repository at current directory'

    def build(self, args: List[str], settings: Settings) -> Command:
        git_path = git_path_from_cwd().replace('/hooks', '')
        git = Git(git_path)
        if '-a' in args or '--alongside' in args:
            strategy = CreateAlongsideHookStrategy(git_path)
        elif '-o' in args or '--overwrite' in args:
            strategy = CreateHookStrategy(git_path)
        elif git.non_guet_hooks_present():
            strategy = PromptUserForHookTypeStrategy(git_path)
        else:
            strategy = CreateHookStrategy(git_path)
        return StrategyCommand(strategy)
