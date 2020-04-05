from unittest import TestCase
from unittest.mock import Mock

from guet.commands.command_factory import CommandFactoryMethod
from guet.commands.strategies.print_strategy import PrintCommandStrategy
from guet.commands.decorators.version_decorator import VersionDecorator
from guet.settings.settings import Settings


class TestVersionDecorator(TestCase):
    def test_build_returns_decorated_build_when_no_version_flags_exist(self):
        decorated: CommandFactoryMethod = Mock()
        decorator = VersionDecorator(decorated)
        args = ['not', 'a', 'version', 'flag']
        settings: Settings = Mock()
        decorator.build(args, settings)
        decorated.build.assert_called_with(args, settings)

    def test_build_returns_print_strategy_if_dash_v_present(self):
        decorated: CommandFactoryMethod = Mock()
        decorator = VersionDecorator(decorated)
        args = ['other', '-v', 'other']
        settings: Settings = Mock()
        result = decorator.build(args, settings)

        decorated.build.assert_not_called()
        self.assertIsInstance(result.strategy, PrintCommandStrategy)

    def test_build_returns_returns_print_strategy_if_dash_dash_version_present(self):
        decorated: CommandFactoryMethod = Mock()
        decorator = VersionDecorator(decorated)
        args = ['other', '--version', 'other']
        settings: Settings = Mock()
        result = decorator.build(args, settings)

        decorated.build.assert_not_called()
        self.assertIsInstance(result.strategy, PrintCommandStrategy)
