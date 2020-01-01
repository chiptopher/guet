import unittest
from unittest.mock import patch

from guet.commands.setcommitters.factory import SetCommittersCommandFactory
from guet.config.committer import Committer
from guet.settings.settings import Settings


@patch('guet.commands.setcommitters.set_committers_strategy.get_committers')
@patch('guet.commands.setcommitters.set_committers_strategy.set_committers')
@patch('guet.commands.setcommitters.set_committers_strategy.set_committer_as_author')
class TestSetCommittersCommand(unittest.TestCase):
    def test_execute_adds_the_first_person_in_the_list_as_the_author_email_and_name(
            self, mock_set_committer_as_author, mock_set_committers, mock_get_committers):
        first_committer = Committer('name1', 'email1', 'initials1')
        mock_get_committers.return_value = [
            first_committer, Committer('name2', 'email2', 'initials2')
        ]

        command = SetCommittersCommandFactory().build(['set', 'initials1', 'initials2'], Settings())
        command.execute()

        mock_set_committer_as_author.assert_called_with(first_committer)

    def test_execute_will_add_a_pair_set_and_committers_to_it(self, mock_set_committer_as_author,
                                                              mock_set_committers,
                                                              mock_get_committers):
        first_committer = Committer('name1', 'email1', 'initials1')
        second_committer = Committer('name2', 'email2', 'initials2')
        mock_get_committers.return_value = [
            Committer('ignored', 'ignored', 'ignored'), first_committer, second_committer
        ]

        command = SetCommittersCommandFactory().build(['set', 'initials1', 'initials2'], Settings())
        command.execute()

        mock_set_committers.assert_called_with([first_committer, second_committer])

    @patch('builtins.print')
    def test_execute_prints_out_error_message_when_the_given_initials_arent_in_the_system(
            self, mock_print, mock_set_committer_as_author, mock_set_committers,
            mock_get_committers):
        mock_get_committers.return_value = [Committer('undesired', 'undesired', 'undesired')]
        command = SetCommittersCommandFactory().build(['set', 'initials'], Settings())
        command.execute()
        mock_print.assert_called_once_with("No committer exists with initials 'initials'")

    @patch('builtins.print')
    def test_execute_failing_doesnt_set_committers_still(self, mock_print,
                                                         mock_set_committer_as_author,
                                                         mock_set_committers, mock_get_committers):
        mock_get_committers.return_value = [Committer('undesired', 'undesired', 'undesired')]
        command = SetCommittersCommandFactory().build(['set', 'initials'], Settings())
        command.execute()
        mock_set_committers.assert_not_called()
        mock_set_committer_as_author.assert_not_called()
