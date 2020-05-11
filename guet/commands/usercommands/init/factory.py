from typing import List

from guet.commands.command import Command
from guet.commands.usercommands.help.help_message_builder import HelpMessageBuilder
from guet.commands.usercommands.init._init_command import InitCommand
from guet.commands.usercommands.usercommand_factory import UserCommandFactory
from guet.settings.settings import Settings

INIT_HELP_MESSAGE = HelpMessageBuilder('guet init', 'Initialized guet for use on this computer.').build()


class InitCommandFactory(UserCommandFactory):

    def short_help_message(self) -> str:
        return 'Initialize guet for use'

    def build(self, args: List[str], settings: Settings) -> Command:
        return InitCommand(self.context)
