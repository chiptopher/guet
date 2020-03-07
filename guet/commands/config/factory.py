from typing import List

from guet.commands.command_factory import CommandFactoryMethod
from guet.commands.config.set_config_strategy import SetConfigStrategy
from guet.commands.help.help_message_builder import HelpMessageBuilder
from guet.commands.strategy_command import StrategyCommand
from guet.settings.settings import Settings

CONFIG_HELP_MESSAGE = HelpMessageBuilder('guet config [--<key>=<value> ...', 'Set a configuration.').build()


class ConfigCommandFactory(CommandFactoryMethod):
    def short_help_message(self):
        return 'Change setting values'

    def build(self, args: List[str], settings: Settings):
        return StrategyCommand(SetConfigStrategy(args, self.context))
