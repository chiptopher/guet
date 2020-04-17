import sys

from guet.commands.decorators.local_decorator import LocalDecorator
from guet.commands.usercommands.get.get_factory import GetCommandFactory, GET_HELP_MESSAGE
from guet.commands.decorators.git_required_decorator import GitRequiredDecorator
from guet.commands.decorators.help_decorator import HelpDecorator
from guet.commands.decorators.init_required_decorator import InitRequiredDecorator
from guet.commands.usercommands.init.factory import InitCommandFactory, INIT_HELP_MESSAGE
from guet.commands.usercommands.remove.factory import REMOVE_HELP_MESSAGE, RemoveCommandFactory
from guet.commands.usercommands.setcommitters.factory import SetCommittersCommandFactory, SET_HELP_MESSAGE
from guet.commands.usercommands.start.factory import StartCommandFactory, START_HELP_MESSAGE
from guet.commands.decorators.start_required_decorator import StartRequiredDecorator
from guet.commands.decorators.version_decorator import VersionDecorator
from guet.executor import Executor
from guet.util.errors import log_on_error
from guet.commands.usercommands.addcommitter.factory import AddCommitterFactory, ADD_COMMITTER_HELP_MESSAGE
from guet.commands.usercommands.config.factory import ConfigCommandFactory, CONFIG_HELP_MESSAGE


def _command_builder_map():
    command_builder_map = dict()
    command_builder_map['add'] = VersionDecorator(
        InitRequiredDecorator(
            LocalDecorator(
                HelpDecorator(AddCommitterFactory(), ADD_COMMITTER_HELP_MESSAGE)
            )
        )
    )

    command_builder_map['init'] = VersionDecorator(
        HelpDecorator(InitCommandFactory(), INIT_HELP_MESSAGE, no_args_valid=True))

    command_builder_map['set'] = VersionDecorator(InitRequiredDecorator(
        StartRequiredDecorator(HelpDecorator(SetCommittersCommandFactory(), SET_HELP_MESSAGE))))

    command_builder_map['start'] = VersionDecorator(InitRequiredDecorator(
        HelpDecorator(
            GitRequiredDecorator(StartCommandFactory()), START_HELP_MESSAGE, no_args_valid=True
        )
    ))
    command_builder_map['config'] = VersionDecorator(
        InitRequiredDecorator(HelpDecorator(ConfigCommandFactory(), CONFIG_HELP_MESSAGE)))

    command_builder_map['get'] = VersionDecorator(
        InitRequiredDecorator(HelpDecorator(GetCommandFactory(), GET_HELP_MESSAGE)))

    command_builder_map['remove'] = VersionDecorator(
        InitRequiredDecorator(HelpDecorator(RemoveCommandFactory(), REMOVE_HELP_MESSAGE)))

    return command_builder_map


@log_on_error
def main():
    command_factory = Executor(_command_builder_map())
    command = command_factory.create(sys.argv[1:])
    command.execute()
