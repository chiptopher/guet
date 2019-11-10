

import sys
import traceback

from guet.commands import AddUserCommand, InitDataSourceCommand, SetCommittersCommand, StartCommand
from guet.commands.config import ConfigSetCommand
from guet.factory import CommandFactory
from guet.util.errors import log_on_error


def _command_builder_map():
    command_builder_map = dict()
    command_builder_map['add'] = AddUserCommand
    command_builder_map['init'] = InitDataSourceCommand
    command_builder_map['set'] = SetCommittersCommand
    command_builder_map['start'] = StartCommand
    command_builder_map['config'] = ConfigSetCommand
    return command_builder_map


@log_on_error
def main():
    command_factory = CommandFactory(_command_builder_map())
    command = command_factory.create(sys.argv[1:])
    command.execute()
