
import unittest

from guet.commands.command import Command
from guet.commands.help import HelpCommand
from guet.factory import CommandFactory


class MockCommand(Command):
    def execute(self):
        pass

    def validate(self, arguments: list):
        return False


class TestCommandFactory(unittest.TestCase):

    def test_create_should_iterate_through_all_commands_and_return_the_one_that_matches(self):

        class MockCommandA(MockCommand):
            def validate(self, arguments: list):
                return True

        args = []
        command_factory = CommandFactory()
        actual_command = command_factory.create(args, MockCommand.__subclasses__())
        self.assertEqual(MockCommandA, actual_command.__class__)

    def test_create_returns_help_command_when_the_arguement_is_not_valid_using_actual_subclasses(self):

        args = []
        command_factory = CommandFactory()
        resulting_command = command_factory.create(args)
        self.assertEqual(HelpCommand, resulting_command.__class__)
