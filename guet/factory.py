
import guet
from guet.commands.command import Command
from guet.commands.command_factory import CommandFactoryMethod
from guet.commands.help.guet_usage import guet_usage
from guet.commands.help_message_strategy import HelpMessageStrategy
from guet.commands.print_strategy import PrintCommandStrategy
from guet.commands.strategy_command import StrategyCommand
from guet.settings.settings import Settings
from guet.config.get_config import get_config
from guet.config.already_initialized import already_initialized


class CommandFactory:
    def __init__(self, command_builder_map):
        self.command_builder_map = command_builder_map

    def create(self, args: list) -> Command:
        if '--version' in args or '-v' in args:
            return StrategyCommand(PrintCommandStrategy(guet.__version__))
        elif already_initialized():
            return self._create_with_settings(args, get_config())
        else:
            return self._create_with_settings(args, Settings())

    def _create_with_settings(self, args: list, settings: Settings) -> Command:
        if len(args) > 0:
            command_arg = args[0]
            command_factory: CommandFactoryMethod = self.command_builder_map[command_arg]
            return command_factory.build(args, settings)
        else:
            return StrategyCommand(HelpMessageStrategy(guet_usage(self.command_builder_map)))
