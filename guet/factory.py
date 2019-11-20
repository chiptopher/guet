from guet.commands import HelpCommand
from guet.commands.command import Command
from guet.settings.settings import Settings


class CommandFactory:
    def __init__(self, command_builder_map):
        self.command_builder_map = command_builder_map

    def create(self, args: list) -> Command:
        if len(args) > 0:
            command_arg = args[0]
            initialized_command = self.command_builder_map[command_arg](args, Settings())
            return initialized_command
        else:
            return HelpCommand(args, Settings(), self.command_builder_map)
