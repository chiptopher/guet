from collections import namedtuple
from typing import List

from guet.commands import CommandFactory
from guet.steps import Step


class CommandMap:
    def __init__(self):
        self._commands = dict()

    def add_command(self, key: str, command: CommandFactory, short_description: str):
        self._commands[key] = _MappedCommand(command, short_description)

    def get_command(self, key: str) -> CommandFactory:
        return self._commands[key].command

    def get_description(self, key: str) -> str:
        return self._commands[key].description

    def all_commands(self) -> List[str]:
        return self._commands.keys()


_MappedCommand = namedtuple('MappedCommand', ['command', 'description'])
