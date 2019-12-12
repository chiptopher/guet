from typing import List

from guet.commands.command import Command
from guet.settings.settings import Settings


class CommandStrategy:
    def apply(self, args: List[str], settings: Settings):
        raise NotImplementedError


class StrategyCommand(Command):

    def __init__(self, args: List[str], settings: Settings, command_strategy: CommandStrategy, args_needed=False):
        super().__init__(args, settings, args_needed=args_needed)
        self.strategy = command_strategy

    def help(self) -> str:
        raise NotImplementedError

    @classmethod
    def help_short(cls) -> str:
        raise NotImplementedError

    def execute_hook(self) -> None:
        self.strategy.apply(self.args, self.settings)
