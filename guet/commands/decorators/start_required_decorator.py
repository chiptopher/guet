from os.path import join
from typing import List

from guet.commands.command import Command
from guet.commands.decorators.command_factory_decorator import CommandFactoryDecorator
from guet.commands.strategies.print_strategy import PrintCommandStrategy
from guet.commands.strategies.strategy_command import StrategyCommand
from guet.git.git import Git
from guet.settings.settings import Settings
from guet.util import project_root

GUET_NOT_STARTED_ERROR = (
    'guet not initialized in this repository. '
    'Please use guet start to initialize repository '
    'for use with guet.'
)

NOT_RAN_IN_ROOT_DIRECTORY_ERROR = (
    'You are not in a directory with a git folder. Change back'
    'to your project\'s root directory.'
)


class StartRequiredDecorator(CommandFactoryDecorator):
    def build(self, args: List[str], settings: Settings) -> Command:
        try:
            git = Git(join(project_root(), '.git'))
        except FileNotFoundError:
            return StrategyCommand(PrintCommandStrategy(NOT_RAN_IN_ROOT_DIRECTORY_ERROR))
        if git.hooks_present():
            return self.decorated.build(args, settings)
        else:
            return StrategyCommand(PrintCommandStrategy(GUET_NOT_STARTED_ERROR))
