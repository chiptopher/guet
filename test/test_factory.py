import unittest
from typing import List
from unittest.mock import patch
from guet.commands.help.guet_usage import guet_usage
from guet.commands.argsettingcommand import ArgSettingCommand
from guet.commands.command_factory import CommandFactoryMethod
from guet.factory import CommandFactory
from guet.settings.settings import Settings


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

    @patch('builtins.print')
    def test_uses_command_builder_map_to_print_help_messages(self, mock_print, mock_get_settings,
                                                             mock_already_init):
        builder_map = dict()
        builder_map['command'] = MockCommandFactory()
        command_factory = CommandFactory(builder_map)
        result = command_factory.create([])
        result.execute()
        mock_print.assert_called_with(guet_usage(builder_map))

    def test_returns_command_using_command_factory_build_method(self, mock_get_settings,
                                                                mock_already_init):
        builder_map = dict()
        builder_map['command'] = MockCommandFactory()
        builder_map['not-command'] = NotMockCommand

        command_factory = CommandFactory(builder_map)
        args = ['command']
        result = command_factory.create(args)
        self.assertEqual(MockCommand, type(result))


class MockCommand(ArgSettingCommand):
    def execute_hook(self) -> None:
        pass

    def help(self) -> str:
        pass

    @classmethod
    def help_short(cls) -> str:
        pass


class NotMockCommand(ArgSettingCommand):
    def execute_hook(self) -> None:
        pass

    def help(self) -> str:
        pass

    @classmethod
    def help_short(cls) -> str:
        pass


class MockCommandFactory(CommandFactoryMethod):
    def short_help_message(self):
        pass

    def build(self, args: List[str], settings: Settings):
        return MockCommand(args, settings)
