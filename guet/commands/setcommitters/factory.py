from typing import List

from guet.commands.command_factory import CommandFactoryMethod
from guet.commands.setcommitters.command import SetCommittersCommand
from guet.settings.settings import Settings


class SetCommittersCommandFactory(CommandFactoryMethod):
    def build(self, args: List[str], settings: Settings):
        return SetCommittersCommand(args, settings)

    def short_help_message(self):
        return 'Set the current committers'
