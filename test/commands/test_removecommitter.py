from unittest import TestCase
from unittest.mock import patch

from guet.commands.remove.factory import RemoveCommandFactory
from guet.config.committer import Committer
from guet.settings.settings import Settings


@patch('guet.commands.command_factory_with_context.Context')
@patch('builtins.print')
@patch('guet.commands.remove.remove_strategy.set_committers')
@patch('guet.commands.remove.remove_strategy.get_committers')
class TestRemoveCommitter(TestCase):

    def test_sets_committers_to_all_committers_without_given_initials(self, mock_get_committers, mock_set_committers,
                                                                      _mock, _1):
        committer1 = Committer(initials='initials1', name='name1', email='email1')
        committer2 = Committer(initials='initials2', name='name2', email='email2')
        mock_get_committers.return_value = [
            committer1,
            committer2
        ]
        command = RemoveCommandFactory().build(['remove', 'initials1'], Settings())
        command.execute()

        mock_set_committers.assert_called_with([committer2])

    def test_prints_error_message_if_given_initials_that_dont_exist(self, mock_get_committers, mock_set_committers,
                                                                    mock_print, _1):
        mock_get_committers.return_value = []
        command = RemoveCommandFactory().build(['remove', 'initials1'], Settings())
        command.execute()

        mock_set_committers.assert_not_called()
        mock_print.assert_called_with(f'No committer exists with initials "initials1"')

    def test_short_help_is_correct(self, _mock1, _mock2, _mock3, _mock4):
        self.assertEqual('Removes committer', RemoveCommandFactory().short_help_message())
