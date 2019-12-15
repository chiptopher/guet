from unittest import TestCase
from unittest.mock import patch

from guet.commands.get.committer_printing_strategy import CommitterPrintingStrategy
from guet.commands.get.get_factory import GetCommandFactory, print_only_initials, print_full_names
from guet.commands.get.invalid_identifier_strategy import InvalidIdentifierStrategy
from guet.commands.help_message_strategy import HelpMessageStrategy
from guet.config.committer import Committer
from guet.settings.settings import Settings


@patch('builtins.print')
@patch('guet.commands.get.get_factory.get_current_committers')
@patch('guet.commands.get.get_factory.get_committers')
class TestGetCommand(TestCase):

    def test_get_prints_all_committers_in_short_list(self, mock_get_committers,
                                                     mock_get_current_committers,
                                                     mock_print):
        committers = [
            Committer('name1', 'email1', 'initials1'),
            Committer('name2', 'email2', 'initials2')
        ]
        mock_get_committers.return_value = committers
        command = GetCommandFactory().build(['get', 'committers', '-l'], Settings())
        command.execute()
        mock_print.assert_called_with('initials1, initials2')

    def test_create_command_returns_command_with_full_committers_when_given_no_l_flag(self, mock_get_committers,
                                                                                      mock_get_current_committers,
                                                                                      mock_print):
        committers = [
            Committer('name1', 'email1', 'initials1'),
            Committer('name2', 'email2', 'initials2')
        ]
        mock_get_committers.return_value = committers
        command = GetCommandFactory().build(['get', 'committers'], Settings())
        command.execute()
        mock_print.assert_any_call('All committers')
        mock_print.assert_any_call(committers[0].pretty())
        mock_print.assert_any_call(committers[1].pretty())

    def test_create_command_creates_command_with_current_committers_short_strategy_when_given_l_flag(self,
                                                                                                     mock_get_committers,
                                                                                                     mock_get_current_committers,
                                                                                                     mock_print):
        committers = [
            Committer('name1', 'email1', 'initials1'),
            Committer('name2', 'email2', 'initials2')
        ]
        mock_get_current_committers.return_value = committers
        command = GetCommandFactory().build(['get', 'current', '-l'], Settings())
        command.execute()
        mock_print.assert_called_with('initials1, initials2')

    def test_create_command_creates_command_with_current_committers_full_strategy_when_given_current_identifier(self,
                                                                                                                mock_get_committers,
                                                                                                                mock_get_current_committers,
                                                                                                                mock_print):
        committers = [
            Committer('name1', 'email1', 'initials1'),
            Committer('name2', 'email2', 'initials2')
        ]
        mock_get_current_committers.return_value = committers
        command = GetCommandFactory().build(['get', 'current'], Settings())
        command.execute()
        mock_print.assert_any_call('Currently set committers')
        mock_print.assert_any_call(committers[0].pretty())
        mock_print.assert_any_call(committers[1].pretty())

    def test_create_command_uses_invalid_identifier_strategy_when_given_invalid_identifier(self, mock_get_committers,
                                                                                           mock_get_current_committers,
                                                                                           mock_print):
        command = GetCommandFactory().build(['get', 'bad_identifer'], Settings())
        command.execute()
        mock_print('Invalid identifier <bad_identifier>')

    def test_create_command_uses_help_message_strategy_when_given_no_identifier(self, mock_get_committers,
                                                                                mock_get_current_committers,
                                                                                mock_print):
        command = GetCommandFactory().build(['get'], Settings())
        self.assertIsInstance(command.strategy, HelpMessageStrategy)
