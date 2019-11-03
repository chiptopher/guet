import unittest

from guet.commands.command import Command
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
