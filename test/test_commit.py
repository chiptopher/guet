import datetime
import sys
import unittest
from unittest.mock import Mock, patch

from guet.commit import PostCommitManager, PreCommitManager
from guet.gateways.gateway import committer_result, PairSetGateway, pair_set_result


@patch('guet.commit.set_committer_as_author')
@patch('guet.commit.set_committers')
@patch('guet.commit.get_committers')
@patch('guet.commit.configure_git_author')
class PostCommitManagerTest(unittest.TestCase):

    def setUp(self) -> None:
        self.commit_manager = PostCommitManager()

    def test_manage_rotates_the_commit_names(self,
                                             mock_configure_git_author,
                                             mock_get_committers,
                                             mock_set_committers,
                                             mock_set_committer_as_author):
        committer1 = committer_result(name='Name', email='email', initials='')
        committer2 = committer_result(name='Name2', email='email', initials='')
        result = [committer1, committer2]

        mock_get_committers.return_value = result

        self.commit_manager.manage()

        mock_set_committers.assert_called_with([committer2, committer1])

    def test_manage_sets_the_new_author_name_and_email(self,
                                                       mock_configure_git_author,
                                                       mock_get_committers,
                                                       mock_set_committers,
                                                       mock_set_committer_as_author):
        committer1 = committer_result(name='Name', email='email', initials='')
        committer2 = committer_result(name='Name2', email='email', initials='')
        result = [committer1, committer2]
        mock_get_committers.return_value = result

        self.commit_manager.manage()
        mock_set_committer_as_author.assert_called_with(committer2)

    def test_manage_configures_git_to_use_new_author(self,
                                                     mock_configure_git_author,
                                                     mock_get_committers,
                                                     mock_set_committers,
                                                     mock_set_committer_as_author):
        committer1 = committer_result(name='Name', email='email', initials='')
        committer2 = committer_result(name='Name2', email='email', initials='')
        result = [committer1, committer2]
        mock_get_committers.return_value = result

        self.commit_manager.manage()
        mock_configure_git_author.assert_called_with(committer2.name, committer2.email)


class PreCommitManagerTest(unittest.TestCase):

    def setUp(self):
        self.mock_pair_set_gateway = PairSetGateway()
        self.mock_pair_set_gateway.get_pair_set = Mock()
        self.mock_pair_set_gateway.add_pair_set = Mock()
        self.mock_pair_set_gateway.get_most_recent_pair_set = Mock()


    @patch('builtins.print')
    @patch('builtins.exit')
    def test_manage_checks_for_most_recent_pair_set_and_exits_1_if_it_is_over_24_hours(self,
                                                                                       mock_exit,
                                                                                       mock_print):
        twenty_four_hours = 86400000
        # offset timestamp by 1 so because test might complete in under a second, causing it to fail
        now = round((datetime.datetime.utcnow().timestamp() - 1) * 1000)

        def _mock_most_recent_pair_set():
            return pair_set_result(id=1, set_time=now - twenty_four_hours)

        self.mock_pair_set_gateway.get_most_recent_pair_set = Mock(side_effect=_mock_most_recent_pair_set)
        subject = PreCommitManager(self.mock_pair_set_gateway)
        subject.manage()
        mock_exit.assert_called_once_with(1)
        mock_print.assert_called_with(
            "\nYou have not reset pairs in over twenty four hours!\nPlease reset your pairs by using guet set and including your pairs' initials\n")

    @patch('builtins.print')
    @patch('builtins.exit')
    def test_manage_checks_for_most_recent_pair_set_and_exits_0_if_it_is_under_24_hours(self,
                                                                                        mock_exit,
                                                                                        mock_print):
        ten_hours = 36000000
        now = round(datetime.datetime.utcnow().timestamp() * 1000)

        def _mock_most_recent_pair_set():
            return pair_set_result(id=1, set_time=now - ten_hours)

        self.mock_pair_set_gateway.get_most_recent_pair_set = Mock(side_effect=_mock_most_recent_pair_set)
        subject = PreCommitManager(self.mock_pair_set_gateway)
        subject.manage()
        mock_exit.assert_called_once_with(0)
