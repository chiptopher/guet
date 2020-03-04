from unittest import TestCase
from unittest.mock import patch, call, Mock

from guet.commands.addcommitter.factory import AddCommitterFactory, ADD_COMMITTER_HELP_MESSAGE
from guet.commands.cancellable_strategy import CancelableCommandStrategy
from guet.config.committer import Committer
from guet.context.context import Context
from guet.settings.settings import Settings


@patch('guet.commands.addcommitter.factory.Context')
@patch('guet.commands.addcommitter.factory.get_committers', return_value=[])
@patch('guet.commands.addcommitter.add_committer_strategy.add_committer')
@patch('builtins.print')
class TestAddCommitterFactory(TestCase):

    def test_returns_cancelable_strategy_if_given_initials_match_already_present_committer(self,
                                                                                           mock_print,
                                                                                           mock_add_committer,
                                                                                           get_committers,
                                                                                           mock_context):
        mock_committers = Mock()
        context: Context = mock_context.instance.return_value
        context.committers = mock_committers
        mock_committers.all.return_value = [Committer(initials='initials', name='name', email='email')]

        subject = AddCommitterFactory()
        response = subject.build(['add', 'initials', 'name', 'email'], Settings())
        self.assertIsInstance(response.strategy, CancelableCommandStrategy)

    def test_execute_prints_error_message_when_too_many_arguments_are_given(
            self, mock_print, mock_add_commiter, mock_get_committers, mock_context):
        initials = 'usr'
        name = 'user'
        email = 'user@localhost'

        command = AddCommitterFactory().build(['add', initials, name, email, 'extra'], Settings())
        command.execute()

        mock_print.assert_called_once_with('Too many arguments.')

    def test_execute_prints_the_error_message_and_help_message_when_there_are_not_enough_args(
            self, mock_print, mock_add_commiter, mock_get_committers, mock_context):
        command = AddCommitterFactory().build(['guet', 'initials', 'name'], Settings())
        command.execute()

        calls = [
            call('Not enough arguments.'),
            call(''),
            call(ADD_COMMITTER_HELP_MESSAGE)
        ]
        mock_print.assert_has_calls(calls)

    def test_get_short_help_message(self, mock_print, mock_add_commiter, mock_get_committers, mock_context):
        self.assertEqual('Add committer to the list of available committers',
                         AddCommitterFactory().short_help_message())

    def test_execute_also_adds_committer_to_committers_file(self, mock_print, mock_add_commiter, mock_get_committers,
                                                            mock_context):
        command = AddCommitterFactory().build(['add', 'initials', 'name', 'email'], Settings())
        command.execute()

        mock_add_commiter.assert_called_with('initials', 'name', 'email')
