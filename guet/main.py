import sys

from guet.commands.get.get_factory import GetCommandFactory
from guet.commands.init_required_decorator import InitRequiredDecorator
from guet.commands.start.factory import StartCommandFactory
from guet.factory import CommandFactory
from guet.util.errors import log_on_error
from guet.commands.addcommitter.factory import AddCommitterFactory
from guet.commands.init.factory import InitCommandFactory
from guet.commands.setcommitters.factory import SetCommittersCommandFactory
from guet.commands.config.factory import ConfigCommandFactory


def _command_builder_map():
    command_builder_map = dict()
    command_builder_map['add'] = InitRequiredDecorator(AddCommitterFactory())
    command_builder_map['init'] = InitCommandFactory()
    command_builder_map['set'] = InitRequiredDecorator(SetCommittersCommandFactory())
    command_builder_map['start'] = InitRequiredDecorator(StartCommandFactory())
    command_builder_map['config'] = InitRequiredDecorator(ConfigCommandFactory())
    command_builder_map['get'] = InitRequiredDecorator(GetCommandFactory())
    return command_builder_map


@log_on_error
def main():
    command_factory = CommandFactory(_command_builder_map())
    command = command_factory.create(sys.argv[1:])
    command.execute()
