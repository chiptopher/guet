from typing import List

from guet.commands.usercommands.config.set_config_strategy import SetConfigStrategy
from guet.commands.strategies.strategy_command import StrategyCommand
from guet.commands.usercommands.help.help_message_builder import HelpMessageBuilder
from guet.commands.usercommands.usercommand_factory import UserCommandFactory
from guet.settings.settings import Settings

CONFIG_HELP_MESSAGE = HelpMessageBuilder('guet config [--<key>=<value> ...', 'Set a configuration.').build()


class ConfigCommandFactory(UserCommandFactory):
    def short_help_message(self):
        return 'Change setting values'

    def build(self, args: List[str], settings: Settings):
        return StrategyCommand(SetConfigStrategy(args, self.context))
