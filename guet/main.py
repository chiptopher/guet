import sys

from guet.util.errors import log_on_error
from guet.util import get_command_key
from guet.commands import CommandMap
from guet.commands.help import HelpCommandFactory
from guet.files import FileSystem

file_system = FileSystem()


@log_on_error
def main():
    command_map = CommandMap()
    command_map.add_command('help', HelpCommandFactory(
        command_map, file_system), 'Display guet usage')
    command = command_map.get_command(get_command_key(sys.argv[1:])).build()
    command.play(sys.argv[1:])
