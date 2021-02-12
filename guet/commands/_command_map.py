from collections import namedtuple
from typing import List

from guet.commands import CommandFactory

_MappedCommand = namedtuple('MappedCommand', ['command', 'description'])


class CommandMap:
    def __init__(self):
        self._commands = dict()
        self._default = None

    def add_command(self, key: str, command: CommandFactory, short_description: str):
        self._commands[key] = _MappedCommand(command, short_description)

    def _get(self, key: str) -> _MappedCommand:
        return self._commands.get(key, self._default)

    def get_command(self, key: str) -> CommandFactory:
        return self._get(key).command

    def get_description(self, key: str) -> str:
        return self._get(key).description

    def all_commands(self) -> List[str]:
        return self._commands.keys()

    def set_default(self, command: CommandFactory):
        self._default = _MappedCommand(command, '')
