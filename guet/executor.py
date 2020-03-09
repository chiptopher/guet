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


class Executor:
    def __init__(self, command_builder_map):
        self.command_builder_map = command_builder_map

    def create(self, args: list) -> Command:
        if already_initialized():
            return self._create_with_settings(args, get_config())
        else:
            return self._create_with_settings(args, Settings())

    def _create_with_settings(self, args: list, settings: Settings) -> Command:
        if len(args) > 0:
            command_arg = args[0]
            if command_arg in ('--version', '-v'):
                return StrategyCommand(PrintCommandStrategy(guet.__version__))
            return self.load_command_factory_from_map(args, settings)
        else:
            return self._guet_ussage_command()

    def load_command_factory_from_map(self, args, settings):
        command_arg = args[0]
        try:
            command_factory: CommandFactoryMethod = self.command_builder_map[command_arg]
            return command_factory.build(args, settings)
        except KeyError:
            return self.load_invalid_command(command_arg)

    def load_invalid_command(self, command_arg: str):
        if command_arg in ('-h', '--help'):
            return self._guet_ussage_command()
        return self._guet_ussage_command(invalid_command=command_arg)

    def _guet_ussage_command(self, *, invalid_command: str = ''):
        message = guet_usage(self.command_builder_map)
        if invalid_command:
            message = f'guet has no command "{invalid_command}" that can be ran.\n\n' + message
        return StrategyCommand(HelpMessageStrategy(message))
