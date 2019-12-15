from unittest import TestCase
from guet.commands.command_factory import CommandFactoryMethod
from unittest.mock import Mock
from guet.commands.command_factory_decorator import CommandFactoryDecorator


class CommandFactoryDecoratorTest(TestCase):
    def test_short_help_message_returns_decorated_message(self):
        mock_command_factory = CommandFactoryMethod()
        mock_command_factory.short_help_message = Mock(return_value='Message')
        command_factory_decorator = CommandFactoryDecorator(mock_command_factory)
        self.assertEqual('Message', command_factory_decorator.short_help_message())