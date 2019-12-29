from guet.commands.command import Command
from guet.commands.strategy import CommandStrategy


class StrategyCommand(Command):
    def __init__(self, command_strategy: CommandStrategy):
        super().__init__()
        self.strategy = command_strategy

    def execute(self):
        self.strategy.apply()
