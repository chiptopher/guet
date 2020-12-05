from unittest import TestCase
from unittest.mock import call, Mock, patch

from guet.commands import CommandMap
from guet.commands.help import UsageAction


class TestUsageAction(TestCase):

    @patch('builtins.print')
    def test_prints_all_descriptions_for_registered_commands(self, mock_print):
        command_map = CommandMap()
        command_map.add_command('test1', Mock(), 'description1')
        command_map.add_command('test2', Mock(), 'description2')

        usage_action = UsageAction(command_map)

        usage_action.execute([])

        mock_print.assert_has_calls([
            call('usage: guet <command>\n'),
            call('test1: description1'),
            call('test2: description2')
        ])
