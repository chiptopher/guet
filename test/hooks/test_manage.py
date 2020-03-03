from unittest import TestCase
from unittest.mock import Mock

from guet.hooks import manage


class TestManage(TestCase):
    def test_manage_calls_hook_method_if_name_is_in_map(self):
        hook_method = Mock()
        name = 'name'
        hook_map = {
            name: hook_method
        }
        manage('name', hook_map=hook_map)
        hook_method.assert_called()

    def test_manage_silently_moves_on_if_name_is_not_in_map(self):
        hook_method = Mock()
        name = 'name'
        hook_map = {
            name: hook_method
        }
        manage('other-name', hook_map=hook_map)
