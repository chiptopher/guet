from typing import List
from guet.commands.command import Command
from guet.settings.settings import Settings


class HelpCommand(Command):

    def __init__(self, args: List[str], settings: Settings, command_builder_map=None):
        super().__init__(args, settings)
        if command_builder_map is None:
            command_builder_map = dict()
        self.command_builder_map = command_builder_map

    def help(self):
        help_message = 'usage: guet <command>\n'
        for key in self.command_builder_map:
            if issubclass(self.command_builder_map[key], Command):
                short_help_message = self.command_builder_map[key].get_short_help_message()
                help_message += '\n   {} -- {}'.format(key, short_help_message)
        return help_message + '\n'

    def execute_hook(self) -> None:
        pass

    @classmethod
    def help_short(cls) -> str:
        pass
