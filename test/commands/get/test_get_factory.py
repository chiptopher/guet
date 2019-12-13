from unittest import TestCase

from guet.commands.get.all_committers_strategy import AllCommittersStrategy
from guet.commands.get.current_committers_strategy import CurrentCommittersStrategy
from guet.commands.get.full_committers_list_strategy import FullCommittersListStrategy
from guet.commands.get.get_factory import GetCommandFactory
from guet.commands.get.invalid_identifier_strategy import InvalidIdentifierStrategy
from guet.commands.get.short_list_strategy import ShortCommittersListStrategy
from guet.commands.help_message_strategy import HelpMessageStrategy
from guet.settings.settings import Settings


class TestGetCommand(TestCase):

    def test_create_command_returns_command_with_short_committers_list_when_given_l_flag(self):
        command = GetCommandFactory().build(['get', 'committers', '-l'], Settings())
        self.assertIsInstance(command.strategy, AllCommittersStrategy)
        self.assertIsInstance(command.strategy.committer_printing_strategy, ShortCommittersListStrategy)

    def test_create_command_returns_command_with_full_committers_when_given_no_l_flag(self):
        command = GetCommandFactory().build(['get', 'committers'], Settings())
        self.assertIsInstance(command.strategy, AllCommittersStrategy)
        self.assertIsInstance(command.strategy.committer_printing_strategy, FullCommittersListStrategy)

    def test_create_command_creates_command_with_current_committers_short_strategy_when_given_l_flag(self):
        command = GetCommandFactory().build(['get', 'current'], Settings())
        self.assertIsInstance(command.strategy, CurrentCommittersStrategy)
        self.assertIsInstance(command.strategy.committer_printing_strategy, FullCommittersListStrategy)

    def test_create_command_creates_command_with_current_committers_full_strategy_when_given_current_identifier(self):
        command = GetCommandFactory().build(['get', 'current', '-l'], Settings())
        self.assertIsInstance(command.strategy, CurrentCommittersStrategy)
        self.assertIsInstance(command.strategy.committer_printing_strategy, ShortCommittersListStrategy)

    def test_create_command_uses_invalid_identifier_strategy_when_given_invalid_identifier(self):
        command = GetCommandFactory().build(['get', 'bad_identifer'], Settings())
        self.assertIsInstance(command.strategy, InvalidIdentifierStrategy)

    def test_create_command_uses_help_message_strategy_when_given_no_identifier(self):
        command = GetCommandFactory().build(['get'], Settings())
        self.assertIsInstance(command.strategy, HelpMessageStrategy)
