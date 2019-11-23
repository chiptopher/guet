import unittest
from unittest.mock import patch
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


@patch('guet.factory.already_initialized', return_value=True)
@patch('guet.factory.get_config')
class TestCommandFactory(unittest.TestCase):
    def test_returns_command_from_builder_method_that_matches(self, mock_get_settings,
                                                              mock_already_init):
        builder_map = dict()
        builder_map['command'] = MockCommand
        builder_map['not-command'] = NotMockCommand

        command_factory = CommandFactory(builder_map)
        args = ['command']
        result = command_factory.create(args)
        self.assertEqual(MockCommand, type(result))

    def test_returns_command_with_settings_from_settings_file(self, mock_get_settings,
                                                              mock_already_init):
        expected_settings = Settings()
        mock_get_settings.return_value = expected_settings
        builder_map = dict()
        builder_map['command'] = MockCommand
        builder_map['not-command'] = NotMockCommand

        command_factory = CommandFactory(builder_map)
        args = ['command']
        result = command_factory.create(args)
        self.assertEqual(expected_settings, result.settings)

    def test_uses_new_settings_with_default_values_if_initialization_hasnt_been_ran(
            self, mock_get_settings, mock_already_init):
        mock_already_init.return_value = False
        returned_settings = Settings()
        mock_get_settings.return_value = returned_settings
        builder_map = dict()
        builder_map['command'] = MockCommand

        command_factory = CommandFactory(builder_map)
        args = ['command']
        result = command_factory.create(args)
        self.assertNotEqual(returned_settings, result.settings)

    def test_returns_help_command_if_no_command_provided(self, mock_get_settings,
                                                         mock_already_init):
        command_factory = CommandFactory(dict())
        result = command_factory.create([])
        self.assertEqual(HelpCommand, type(result))

    def test_help_command_has_command_builder_map(self, mock_get_settings, mock_already_init):
        mock_get_settings.return_value = Settings()
        command_builder_map = dict()
        command_builder_map['command'] = lambda args, settings: Command(args, settings)
        command_factory = CommandFactory(command_builder_map)
        result = command_factory.create([])
        self.assertEqual(command_builder_map, result.command_builder_map)
