import datetime
import time
import unittest
from unittest.mock import Mock, patch

from guet.commit import PostCommitManager, PreCommitManager
from guet.config.committer import Committer
from guet.currentmillis import current_millis


@patch('guet.commit.set_committer_as_author')
@patch('guet.commit.set_current_committers')
@patch('guet.commit.get_current_committers')
@patch('guet.commit.configure_git_author')
class PostCommitManagerTest(unittest.TestCase):

    def setUp(self) -> None:
        self.commit_manager = PostCommitManager()

    def test_manage_rotates_the_commit_names(self,
                                             mock_configure_git_author,
                                             mock_get_committers,
                                             mock_set_committers,
                                             mock_set_committer_as_author):
        committer1 = Committer(name='Name', email='email', initials='')
        committer2 = Committer(name='Name2', email='email', initials='')
        result = [committer1, committer2]

        mock_get_committers.return_value = result

        self.commit_manager.manage()

        mock_set_committers.assert_called_with([committer2, committer1])

    def test_manage_sets_the_new_author_name_and_email(self,
                                                       mock_configure_git_author,
                                                       mock_get_committers,
                                                       mock_set_committers,
                                                       mock_set_committer_as_author):
        committer1 = Committer(name='Name', email='email', initials='')
        committer2 = Committer(name='Name2', email='email', initials='')
        result = [committer1, committer2]
        mock_get_committers.return_value = result

        self.commit_manager.manage()
        mock_set_committer_as_author.assert_called_with(committer2)

    def test_manage_configures_git_to_use_new_author(self,
                                                     mock_configure_git_author,
                                                     mock_get_committers,
                                                     mock_set_committers,
                                                     mock_set_committer_as_author):
        committer1 = Committer(name='Name', email='email', initials='')
        committer2 = Committer(name='Name2', email='email', initials='')
        result = [committer1, committer2]
        mock_get_committers.return_value = result

        self.commit_manager.manage()
        mock_configure_git_author.assert_called_with(committer2.name, committer2.email)


class PreCommitManagerTest(unittest.TestCase):

    @patch('guet.commit.most_recent_committers_set')
    @patch('builtins.print')
    @patch('builtins.exit')
    def test_manage_checks_for_most_recent_pair_set_and_exits_1_if_it_is_over_24_hours(self,
                                                                                       mock_exit,
                                                                                       mock_print,
                                                                                       mock_most_recent_committers_set):
        twenty_four_hours = 86400000
        now = current_millis()
        mock_most_recent_committers_set.return_value = now - 100 - twenty_four_hours

        subject = PreCommitManager()
        subject.manage()
        mock_exit.assert_called_once_with(1)
        mock_print.assert_called_with(
            "\nYou have not reset pairs in over twenty four hours!\nPlease reset your pairs by using guet set and including your pairs' initials\n")

    @patch('guet.commit.most_recent_committers_set')
    @patch('builtins.print')
    @patch('builtins.exit')
    def test_manage_checks_for_most_recent_pair_set_and_exits_0_if_it_is_under_24_hours(self,
                                                                                        mock_exit,
                                                                                        mock_print,
                                                                                        mock_most_recent_committers_set):
        ten_hours = 36000000
        now = round((datetime.datetime.utcnow().timestamp() - 1) * 1000)
        mock_most_recent_committers_set.return_value = now - ten_hours
        subject = PreCommitManager()
        subject.manage()

        mock_exit.assert_called_once_with(0)
