from unittest.mock import Mock, patch

from guet.commands.setcommitters import SetCommittersCommand
from guet.config.committer import Committer
from test.commands.test_command import CommandTest, create_test_case


@patch('guet.commands.setcommitters.get_committers')
@patch('guet.commands.setcommitters.set_committers')
@patch('guet.commands.setcommitters.set_committer_as_author')
class TestSetCommittersCommand(CommandTest):

    def test_validate(self,
                      mock_set_committer_as_author,
                      mock_set_committers,
                      mock_get_committers):
        cases = [
            create_test_case(['set', 'extra'], True, 'Should return true when the correct number of args'),
            create_test_case([], False, 'Should return false when not enough arguments are given'),
            create_test_case(['something else'], False, 'Should return false when the required args are wrong')
        ]

        for case in cases:
            self._validate_test(case, SetCommittersCommand)

    def test_execute_adds_the_first_person_in_the_list_as_the_author_email_and_name(self,
                                                                                    mock_set_committer_as_author,
                                                                                    mock_set_committers,
                                                                                    mock_get_committers):
        first_committer = Committer('name1', 'email1', 'initials1')
        mock_get_committers.return_value = [
            first_committer,
            Committer('name2', 'email2', 'initials2')
        ]

        command = SetCommittersCommand(['set', 'initials1', 'initials2'])
        command.execute()

        mock_set_committer_as_author.assert_called_with(first_committer)

    def test_execute_will_add_a_pair_set_and_committers_to_it(self,
                                                              mock_set_committer_as_author,
                                                              mock_set_committers,
                                                              mock_get_committers):
        first_committer = Committer('name1', 'email1', 'initials1')
        second_committer = Committer('name2', 'email2', 'initials2')
        mock_get_committers.return_value = [
            Committer('ignored', 'ignored', 'ignored'),
            first_committer,
            second_committer
        ]

        command = SetCommittersCommand(['set', 'initials1', 'initials2'])
        command.execute()

        mock_set_committers.assert_called_with([first_committer, second_committer])

    @patch('builtins.print')
    def test_execute_prints_out_error_message_when_the_given_initials_arent_in_the_system(self,
                                                                                          mock_print,
                                                                                          mock_set_committer_as_author,
                                                                                          mock_set_committers,
                                                                                          mock_get_committers):
        mock_get_committers.return_value = [
            Committer('undesired', 'undesired', 'undesired')
        ]
        command = SetCommittersCommand(['set', 'initials'])
        command.execute()
        mock_print.assert_called_once_with("No committer exists with initials 'initials'")

    @patch('builtins.print')
    def test_execute_failing_doesnt_set_committers_still(self,
                                                         mock_print,
                                                         mock_set_committer_as_author,
                                                         mock_set_committers,
                                                         mock_get_committers):
        mock_get_committers.return_value = [
            Committer('undesired', 'undesired', 'undesired')
        ]
        command = SetCommittersCommand(['set', 'initials'])
        command.execute()
        mock_set_committers.assert_not_called()
        mock_set_committer_as_author.assert_not_called()
