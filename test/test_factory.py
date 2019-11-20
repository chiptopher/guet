import unittest

from guet.commands import HelpCommand
from guet.commands.command import Command
from guet.factory import CommandFactory
from guet.settings.settings import Settings


class MockCommand(Command):
    def execute_hook(self) -> None:
        pass

    def help(self) -> str:
        pass

    @classmethod
    def help_short(cls) -> str:
        pass


class NotMockCommand(Command):
    def execute_hook(self) -> None:
        pass

    def help(self) -> str:
        pass

    @classmethod
    def help_short(cls) -> str:
        pass


class TestCommandFactory(unittest.TestCase):

    def test_returns_command_from_builder_method_that_matches(self):
        builder_map = dict()
        builder_map['command'] = MockCommand
        builder_map['not-command'] = NotMockCommand

        command_factory = CommandFactory(builder_map)
        args = ['command']
        result = command_factory.create(args)
        self.assertEqual(MockCommand, type(result))

    def test_returns_help_command_if_no_command_provided(self):
        command_factory = CommandFactory(dict())
        result = command_factory.create([])
        self.assertEqual(HelpCommand, type(result))

    def test_help_command_has_command_builder_map(self):
        command_builder_map = dict()
        command_builder_map['command'] = lambda args: Command(args, Settings())
        command_factory = CommandFactory(command_builder_map)
        result = command_factory.create([])
        self.assertEqual(command_builder_map, result.command_builder_map)
