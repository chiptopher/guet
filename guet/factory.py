from guet.commands import HelpCommand
from guet.commands.command import Command
from guet.settings.settings import Settings
from guet.config.get_config import get_config
from guet.config.already_initialized import already_initialized


class CommandFactory:
    def __init__(self, command_builder_map):
        self.command_builder_map = command_builder_map

    def create(self, args: list) -> Command:
        result = None
        if already_initialized():
            result = self._create_with_settings(args, get_config())
        else:
            result = self._create_with_settings(args, Settings())
        return result

    def _create_with_settings(self, args: list, settings: Settings) -> Command:
        if len(args) > 0:
            command_arg = args[0]
            command = self.command_builder_map[command_arg](args, settings)
            return command
        else:
            return HelpCommand(args, Settings(), self.command_builder_map)
