from typing import List

from guet.commands.command import Command
from guet.commands.command_factory import CommandFactoryMethod
from guet.commands.help.help_message_builder import HelpMessageBuilder, FlagBuilder, FlagsBuilder
from guet.commands.print_strategy import PrintCommandStrategy
from guet.commands.start.create_alongside_hook_strategy import CreateAlongsideHookStrategy
from guet.commands.start.create_hook_strategy import CreateHookStrategy
from guet.commands.start.start_strategy import PromptUserForHookTypeStrategy
from guet.commands.strategy_command import StrategyCommand
from guet.git.any_hooks_present import any_hooks_present
from guet.git.git_path_from_cwd import git_hook_path_from_cwd
from guet.git.git_present_in_cwd import git_present_in_cwd
from guet.settings.settings import Settings

START_HELP_MESSAGE = HelpMessageBuilder('guet start',
                                        'Initialize current .git project to use guet.') \
    .flags(FlagsBuilder(
    [FlagBuilder('-a/--alongside', 'Create hooks alongside current hooks with "-guet" on the end'),
     FlagBuilder('-o/--overwrite', 'Overwrite current hooks')])).build()


class StartCommandFactory(CommandFactoryMethod):
    def short_help_message(self) -> str:
        return 'Start guet usage in the repository at current directory'

    def build(self, args: List[str], settings: Settings) -> Command:
        if git_present_in_cwd():
            hook_path = git_hook_path_from_cwd()
            if '-a' in args or '--alongside' in args:
                strategy = CreateAlongsideHookStrategy(hook_path)
            elif '-o' in args or '--overwrite' in args:
                strategy = CreateHookStrategy(hook_path)
            elif not any_hooks_present(hook_path):
                strategy = CreateHookStrategy(hook_path)
            else:
                strategy = PromptUserForHookTypeStrategy(hook_path)
            return StrategyCommand(strategy)
        else:
            return StrategyCommand(PrintCommandStrategy('Git not initialized in this directory.'))
