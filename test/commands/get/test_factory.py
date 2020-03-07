from unittest import TestCase
from unittest.mock import patch, Mock

from guet.commands.get.get_factory import GetCommandFactory
from guet.config.committer import Committer
from guet.context.context import Context
from guet.settings.settings import Settings


@patch('builtins.print')
@patch('guet.commands.get.get_factory.get_current_committers')
@patch('guet.commands.command_factory.Context')
class TestGetCommand(TestCase):

    def test_get_prints_all_committers_in_short_list(self, mock_context,
                                                     mock_get_current_committers,
                                                     mock_print):
        mock_committers = Mock()
        context: Context = mock_context.instance.return_value
        context.committers = mock_committers
        committers = [
            Committer('name1', 'email1', 'initials1'),
            Committer('name2', 'email2', 'initials2')
        ]
        mock_committers.all.return_value = committers
        command = GetCommandFactory().build(['get', 'committers', '-l'], Settings())
        command.execute()
        mock_print.assert_called_with('initials1, initials2')

    def test_create_command_returns_command_with_full_committers_when_given_no_l_flag(self, mock_context,
                                                                                      mock_get_current_committers,
                                                                                      mock_print):
        mock_committers = Mock()
        context: Context = mock_context.instance.return_value
        context.committers = mock_committers
        committers = [
            Committer('name1', 'email1', 'initials1'),
            Committer('name2', 'email2', 'initials2')
        ]
        context.committers.return_value = committers
        mock_committers.all.return_value = committers
        command = GetCommandFactory().build(['get', 'committers'], Settings())
        command.execute()
        mock_print.assert_any_call('All committers')
        mock_print.assert_any_call(committers[0].pretty())
        mock_print.assert_any_call(committers[1].pretty())

    def test_create_command_creates_command_with_current_committers_short_strategy_when_given_l_flag(self,
                                                                                                     mock_context,
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
                                                                                                                mock_context,
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

    def test_create_command_uses_invalid_identifier_strategy_when_given_invalid_identifier(self, mock_context,
                                                                                           mock_get_current_committers,
                                                                                           mock_print):
        command = GetCommandFactory().build(['get', 'bad_identifer'], Settings())
        command.execute()
        mock_print('Invalid identifier <bad_identifier>')
