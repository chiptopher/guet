from typing import List

from guet.commands.argsettingcommand import ArgSettingCommand
from guet.commands.command import Command
from guet.commands.command_factory import CommandFactoryMethod
from guet.commands.help.guet_usage import guet_usage
from guet.commands.help_message_strategy import HelpMessageStrategy
from guet.commands.strategy_command import StrategyCommand
from guet.settings.settings import Settings
from guet.config.get_config import get_config
from guet.config.already_initialized import already_initialized


class CommandFactory:
    def __init__(self, command_builder_map):
        self.command_builder_map = command_builder_map

    def create(self, args: list) -> ArgSettingCommand:
        result = None
        if already_initialized():
            result = self._create_with_settings(args, get_config())
        else:
            result = self._create_with_settings(args, Settings())
        return result

    def _create_with_settings(self, args: list, settings: Settings) -> Command:
        if len(args) > 0:
            command_arg = args[0]
            command_type = self.command_builder_map[command_arg]
            if isinstance(command_type, CommandFactoryMethod):
                return self._create_with_command_factory(command_type, args, settings)
            else:
                return self._create_with_command_constructor(command_type, args, settings)

        else:
            return StrategyCommand(HelpMessageStrategy(guet_usage(self.command_builder_map)))

    def _create_with_command_constructor(self, command_class, args: List[str],
                                         settings: Settings) -> ArgSettingCommand:
        return command_class(args, settings)

    def _create_with_command_factory(self, command_factory: CommandFactoryMethod, args: List[str],
                                     settings: Settings) -> ArgSettingCommand:
        return command_factory.build(args, settings)
