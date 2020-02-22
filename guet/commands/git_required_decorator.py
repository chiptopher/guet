from os import getcwd
from os.path import join
from typing import List

from guet.commands.command import Command
from guet.commands.command_factory_decorator import CommandFactoryDecorator
from guet.commands.print_strategy import PrintCommandStrategy
from guet.commands.strategy_command import StrategyCommand
from guet.git.errors import NoGitPresentError
from guet.git.git import Git
from guet.settings.settings import Settings


class GitRequiredDecorator(CommandFactoryDecorator):
    def build(self, args: List[str], settings: Settings) -> Command:
        try:
            Git(join(getcwd(), '.git'))
            return self.decorated.build(args, settings)
        except NoGitPresentError:
            return StrategyCommand(PrintCommandStrategy('Git not initialized in this directory.'))
