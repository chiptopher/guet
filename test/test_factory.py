import unittest

from guet.commands import HelpCommand
from guet.commands.command import Command, Command2
from guet.factory import CommandFactory


class MockCommand(Command):
    def execute(self):
        pass

    def validate(self, arguments: list):
        return False


class NotMockCommand(Command):
    def execute(self):
        pass

    def validate(self, arguments: list):
        return False


class TestCommandFactory(unittest.TestCase):

    def test_returns_command_from_builder_method_that_matches(self):
        builder_map = dict()
        builder_map['command'] = MockCommand
        builder_map['not-command'] = NotMockCommand

        command_factory = CommandFactory(builder_map)
        args = ['command']
        result = command_factory.create(args)
        self.assertEqual(MockCommand, type(result))
        self.assertEqual(args, result._args)

    def test_returns_help_command_if_no_command_provided(self):
        command_factory = CommandFactory(dict())
        result = command_factory.create([])
        self.assertEqual(HelpCommand, type(result))

    def test_help_command_has_command_builder_map(self):
        command_builder_map = dict()
        command_builder_map['command'] = lambda args: Command2(args)
        command_factory = CommandFactory(command_builder_map)
        result = command_factory.create([])
        self.assertEqual(command_builder_map, result.command_builder_map)
