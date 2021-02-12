from guet.commands import CommandFactory, CommandMap
from guet.steps import Step
from guet.steps.action import PrintAction

from ._usage import UsageAction


class UnknownCommandFactory(CommandFactory):
    def __init__(self, command_map: CommandMap):
        self.command_map = command_map

    def build(self) -> Step:
        return PrintAction('Not a valid guet command.\n') \
            .next(UsageAction(self.command_map))
