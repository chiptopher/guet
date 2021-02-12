from unittest import TestCase
from unittest.mock import Mock

from guet.commands import CommandMap
from guet.steps import Step


class TestCommandMap(TestCase):
    def test_add_command_adds_command_to_cache(self):
        command_map = CommandMap()
        command = Mock()
        description = "short description"
        command_map.add_command('init', command, description)

        self.assertEqual(command_map.get_command('init'), command)
        self.assertEqual(command_map.get_description('init'), description)
