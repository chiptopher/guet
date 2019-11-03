

import sys

from guet.commands import AddUserCommand, InitDataSourceCommand, SetCommittersCommand, StartCommand
from guet.factory import CommandFactory


def _command_builder_map():
    command_builder_map = dict()
    command_builder_map['add'] = AddUserCommand
    command_builder_map['init'] = InitDataSourceCommand
    command_builder_map['set'] = SetCommittersCommand
    command_builder_map['start'] = StartCommand
    return command_builder_map


def main():
    command_factory = CommandFactory(_command_builder_map())
    command = command_factory.create(sys.argv[1:])
    command.execute()
