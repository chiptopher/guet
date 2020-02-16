import sys

from guet.commands.get.get_factory import GetCommandFactory, GET_HELP_MESSAGE
from guet.commands.git_required_decorator import GitRequiredDecorator
from guet.commands.help_decorator import HelpDecorator
from guet.commands.init_required_decorator import InitRequiredDecorator
from guet.commands.remove.factory import RemoveCommandFactory, REMOVE_HELP_MESSAGE
from guet.commands.start.factory import StartCommandFactory, START_HELP_MESSAGE
from guet.commands.start_required_decorator import StartRequiredDecorator
from guet.factory import CommandFactory
from guet.util.errors import log_on_error
from guet.commands.addcommitter.factory import AddCommitterFactory, ADD_COMMITTER_HELP_MESSAGE
from guet.commands.init.factory import InitCommandFactory, INIT_HELP_MESSAGE
from guet.commands.setcommitters.factory import SetCommittersCommandFactory, SET_HELP_MESSAGE
from guet.commands.config.factory import ConfigCommandFactory, CONFIG_HELP_MESSAGE


def _command_builder_map():
    command_builder_map = dict()
    command_builder_map['add'] = InitRequiredDecorator(HelpDecorator(AddCommitterFactory(), ADD_COMMITTER_HELP_MESSAGE))

    command_builder_map['init'] = HelpDecorator(InitCommandFactory(), INIT_HELP_MESSAGE, no_args_valid=True)

    command_builder_map['set'] = InitRequiredDecorator(
        StartRequiredDecorator(HelpDecorator(SetCommittersCommandFactory(), SET_HELP_MESSAGE)))

    command_builder_map['start'] = InitRequiredDecorator(
        HelpDecorator(
            GitRequiredDecorator(StartCommandFactory()), START_HELP_MESSAGE, no_args_valid=True
        )
    )
    command_builder_map['config'] = InitRequiredDecorator(HelpDecorator(ConfigCommandFactory(), CONFIG_HELP_MESSAGE))

    command_builder_map['get'] = InitRequiredDecorator(HelpDecorator(GetCommandFactory(), GET_HELP_MESSAGE))

    command_builder_map['remove'] = InitRequiredDecorator(HelpDecorator(RemoveCommandFactory(), REMOVE_HELP_MESSAGE))

    return command_builder_map


@log_on_error
def main():
    command_factory = CommandFactory(_command_builder_map())
    command = command_factory.create(sys.argv[1:])
    command.execute()
