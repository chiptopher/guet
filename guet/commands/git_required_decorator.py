from typing import List

from guet.commands.command import Command
from guet.commands.command_factory_decorator import CommandFactoryDecorator
from guet.commands.print_strategy import PrintCommandStrategy
from guet.commands.strategy_command import StrategyCommand
from guet.git.git_present_in_cwd import git_present_in_cwd
from guet.settings.settings import Settings


class GitRequiredDecorator(CommandFactoryDecorator):
    def build(self, args: List[str], settings: Settings) -> Command:
        if git_present_in_cwd():
            return self.decorated.build(args, settings)
        else:
            return StrategyCommand(PrintCommandStrategy('Git not initialized in this directory.'))
