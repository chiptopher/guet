
import datetime
import sys
import unittest
from unittest.mock import Mock

from guet.commit import PostCommitManager, PreCommitManager
from guet.gateways.gateway import FileGateway, committer_result, PairSetGateway, pair_set_result
from guet.gateways.io import PrintGateway


class PostCommitManagerTest(unittest.TestCase):

    def setUp(self):
        self.mock_file_gateway = FileGateway()
        self.mock_file_gateway.get_committers = Mock()
        self.mock_file_gateway.set_committers = Mock()
        self.mock_file_gateway.set_author_name = Mock()
        self.mock_file_gateway.set_author_email = Mock()

        self.commit_manager = PostCommitManager(self.mock_file_gateway)

    def test_manage_rotates_the_commit_names(self):
        committer1 = committer_result(name='Name', email='email', initials='')
        committer2 = committer_result(name='Name2', email='email', initials='')
        result = [committer1, committer2]
        self.mock_file_gateway.get_committers = Mock(return_value=result)

        self.commit_manager.manage()
        self.mock_file_gateway.set_committers.assert_called_once_with([committer2, committer1])

    def test_manage_sets_the_new_author_name_and_email(self):
        committer1 = committer_result(name='Name', email='email', initials='')
        committer2 = committer_result(name='Name2', email='email', initials='')
        result = [committer1, committer2]
        self.mock_file_gateway.get_committers = Mock(return_value=result)

        self.commit_manager.manage()
        self.mock_file_gateway.set_author_email.assert_called_once_with(committer2.email)
        self.mock_file_gateway.set_author_name.assert_called_once_with(committer2.name)


class PreCommitManagerTest(unittest.TestCase):

    def tearDown(self):
        sys.stdout = self.original_stdout

    def setUp(self):
        self.mock_pair_set_gateway = PairSetGateway()
        self.mock_pair_set_gateway.get_pair_set = Mock()
        self.mock_pair_set_gateway.add_pair_set = Mock()
        self.mock_pair_set_gateway.get_most_recent_pair_set = Mock()

        self.mock_print_gateway = PrintGateway()
        self.mock_print_gateway.print = Mock()

        self.mock_exit_method = Mock()
        self.original_stdout = sys.stdout

    def test_manage_checks_for_most_recent_pair_set_and_exits_1_if_it_is_over_24_hours(self):
        twenty_four_hours = 86400000
        # offset timestamp by 1 so because test might complete in under a second, causing it to fail
        now = round((datetime.datetime.utcnow().timestamp()-1)*1000)

        def _mock_most_recent_pair_set():
            return pair_set_result(id=1, set_time=now - twenty_four_hours)
        self.mock_pair_set_gateway.get_most_recent_pair_set = Mock(side_effect=_mock_most_recent_pair_set)
        subject = PreCommitManager(self.mock_pair_set_gateway, self.mock_print_gateway, self.mock_exit_method)
        subject.manage()
        self.mock_exit_method.assert_called_once_with(1)
        self.mock_print_gateway.print.assert_called_once_with("\nYou have not reset pairs in over twenty four hours!\nPlease reset your pairs by using guet set and including your pairs' initials\n")

    def test_manage_checks_for_most_recent_pair_set_and_exits_0_if_it_is_under_24_hours(self):
        ten_hours = 36000000
        now = round(datetime.datetime.utcnow().timestamp()*1000)

        def _mock_most_recent_pair_set():
            return pair_set_result(id=1, set_time=now - ten_hours)
        self.mock_pair_set_gateway.get_most_recent_pair_set = Mock(side_effect=_mock_most_recent_pair_set)
        subject = PreCommitManager(self.mock_pair_set_gateway, self.mock_print_gateway, self.mock_exit_method)
        subject.manage()
        self.mock_exit_method.assert_called_once_with(0)
