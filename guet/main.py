import sys

from guet.commands.config.command import ConfigSetCommand
from guet.commands.get.get_factory import GetCommandFactory
from guet.commands.init_required_decorator import InitRequiredDecorator
from guet.factory import CommandFactory
from guet.util.errors import log_on_error
from guet.commands.addcommitter.factory import AddCommitterFactory
from guet.commands.init import InitDataSourceCommand
from guet.commands.setcommitters import SetCommittersCommand
from guet.commands.start import StartCommand
from guet.commands.config.factory import ConfigCommandFactory


def _command_builder_map():
    command_builder_map = dict()
    command_builder_map['add'] = InitRequiredDecorator(AddCommitterFactory())
    command_builder_map['init'] = InitDataSourceCommand
    command_builder_map['set'] = SetCommittersCommand
    command_builder_map['start'] = StartCommand
    command_builder_map['config'] = ConfigCommandFactory()
    command_builder_map['get'] = InitRequiredDecorator(GetCommandFactory())
    return command_builder_map


@log_on_error
def main():
    command_factory = CommandFactory(_command_builder_map())
    command = command_factory.create(sys.argv[1:])
    command.execute()
