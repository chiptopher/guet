from collections import namedtuple
from guet.steps import Step


class CommandMap:
    def __init__(self):
        self._commands = dict()

    def add_command(self, key: str, command: Step, short_description: str):
        self._commands[key] = _MappedCommand(command, short_description)

    def get_command(self, key: str) -> Step:
        return self._commands[key].command

    def get_description(self, key: str) -> str:
        return self._commands[key].description


_MappedCommand = namedtuple('MappedCommand', ['command', 'description'])
