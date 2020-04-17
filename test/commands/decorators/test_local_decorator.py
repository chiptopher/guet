from unittest import TestCase
from unittest.mock import Mock, patch

from guet.settings.settings import Settings

from guet.commands.decorators.local_decorator import LocalDecorator


class LocalDecoratorTest(TestCase):

    def test_calls_build_on_decorated_when_local_flag_not_in_args(self):
        mock_factory = Mock()
        mock_command = Mock()
        mock_factory.build.return_value = mock_command
        decorator = LocalDecorator(mock_factory)
        self.assertEqual(mock_command, decorator.build(['args', 'without', 'flag'], Settings()))

    @patch('guet.commands.decorators.local_decorator.StartRequiredDecorator')
    def test_wraps_decorated_in_start_required_decorator_and_calls_build_when_local_flag_present(self,
                                                                                                 mock_start_required_decorator):
        mock_factory = Mock()
        mock_command = Mock()
        mock_factory.build.return_value = mock_command
        decorator = LocalDecorator(mock_factory)
        mock_start_decorator_instance = mock_start_required_decorator.return_value
        self.assertEqual(mock_start_decorator_instance.build.return_value,
                         decorator.build(['args', 'with', '--local', 'flag'], Settings()))
