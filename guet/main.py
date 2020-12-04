import sys

from guet.util.errors import log_on_error
from guet.util import get_command_key
from guet.commands import CommandMap


@log_on_error
def main():
    command_map = CommandMap()
    command = command_map.get_command(get_command_key(sys.argv))
    command.play(sys.argv[1:])
