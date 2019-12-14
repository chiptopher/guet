from unittest import TestCase
from unittest.mock import Mock, patch

from guet.commands.command_factory import CommandFactoryMethod
from guet.commands.init_required_decorator import InitRequiredDecorator
from guet.settings.settings import Settings


@patch('builtins.exit')
@patch('builtins.print')
@patch('guet.commands.init_required_decorator.already_initialized')
class InitRequriedDecoratorTest(TestCase):
    def test_only_builds_if_already_initialized_is_true(self, mock_already_initialized, mock_print, mock_exit):
        mock_already_initialized.return_value = True
        mock_factory = CommandFactoryMethod()
        mock_factory.build = Mock()
        decorated_factory = InitRequiredDecorator(mock_factory)
        args = []
        settings = Settings()
        decorated_factory.build(args, settings)
        mock_factory.build.assert_called_once_with(args, settings)

    def test_does_not_build_if_not_already_initialized(self, mock_already_initialized, mock_print, mock_exit):
        mock_already_initialized.return_value = False
        mock_factory = CommandFactoryMethod()
        mock_factory.build = Mock()
        decorated_factory = InitRequiredDecorator(mock_factory)
        decorated_factory.build([], Settings())
        mock_factory.build.assert_not_called()

    def test_prints_error_message_when_not_building(self, mock_already_initialized, mock_print, mock_exit):
        mock_already_initialized.return_value = False
        mock_factory = CommandFactoryMethod()
        mock_factory.build = Mock()
        decorated_factory = InitRequiredDecorator(mock_factory)
        decorated_factory.build([], Settings())
        mock_print.assert_called_with(('guet has not been initialized yet! ' +
                                       'Please do so by running the command "guet init".'))
