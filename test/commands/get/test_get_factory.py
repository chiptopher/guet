from unittest import TestCase

from guet.commands.get.all_committers_strategy import AllCommittersStrategy
from guet.commands.get.get_factory import GetCommandFactory
from guet.settings.settings import Settings


class TestGetCommand(TestCase):

    def test_create_command_returns_command_with_short_committers_list_when_given_l_flag(self):
        command = GetCommandFactory().build(['get', 'committers', '-l'], Settings())
        self.assertIsInstance(command.strategy, AllCommittersStrategy)

    def test_create_command_returns_command_with_full_committers_when_given_no_l_flag(self):
        command = GetCommandFactory().build(['get', 'committers'], Settings())
        self.assertIsInstance(command.strategy, AllCommittersStrategy)
