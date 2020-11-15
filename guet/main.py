import sys
from pathlib import Path
from os import getcwd

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
from guet.commands.command import Command
from guet.commands.command_factory import CommandFactoryMethod
from guet.commands.usercommands.addcommitter.factory import AddCommitterFactory, ADD_COMMITTER_HELP_MESSAGE
from guet.commands.usercommands.config.factory import ConfigCommandFactory, CONFIG_HELP_MESSAGE
from guet.steps.check.git_required_check import GitRequiredCheck
from guet.steps.check.help_check import HelpCheck
from guet.steps.check.version_check import VersionCheck
from guet.steps.preparation.initialize import InitializePreparation
from guet.steps.action.start.start import StartAction
from guet.files import FileSystem


start_steps = VersionCheck() \
    .next(HelpCheck(START_HELP_MESSAGE)) \
    .next(InitializePreparation(FileSystem())) \
    .next(GitRequiredCheck(Path(getcwd()).joinpath('.git'))) \
    .next(StartAction(StartCommandFactory()))

def _command_builder_map():
    command_builder_map = dict()
    command_builder_map['add'] = VersionDecorator(
        InitRequiredDecorator(
            LocalDecorator(
                HelpDecorator(AddCommitterFactory(),
                              ADD_COMMITTER_HELP_MESSAGE)
            )
        )
    )

    command_builder_map['init'] = VersionDecorator(
        HelpDecorator(InitCommandFactory(), INIT_HELP_MESSAGE, no_args_valid=True))

    command_builder_map['set'] = VersionDecorator(InitRequiredDecorator(
        StartRequiredDecorator(HelpDecorator(SetCommittersCommandFactory(), SET_HELP_MESSAGE))))

    command_builder_map['start'] = StepsFactory(start_steps)

    command_builder_map['config'] = VersionDecorator(
        InitRequiredDecorator(HelpDecorator(ConfigCommandFactory(), CONFIG_HELP_MESSAGE)))

    command_builder_map['get'] = VersionDecorator(
        InitRequiredDecorator(HelpDecorator(GetCommandFactory(), GET_HELP_MESSAGE)))

    command_builder_map['remove'] = VersionDecorator(
        InitRequiredDecorator(HelpDecorator(RemoveCommandFactory(), REMOVE_HELP_MESSAGE)))

    return command_builder_map


class StepsCommand(Command):
    def __init__(self, args, steps):
        self._args = args
        self._steps = steps

    def execute(self):
        self._steps.play(self._args)


class StepsFactory(CommandFactoryMethod):
    def __init__(self, steps):
        self._steps = steps

    def build(self, args, settings):
        return StepsCommand(args, self._steps)


@log_on_error
def main():
    command_factory = Executor(_command_builder_map())
    command = command_factory.create(sys.argv[1:])
    command.execute()
