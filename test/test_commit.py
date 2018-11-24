
import unittest
from unittest.mock import Mock
from guet.gateway import FileGateway, committer_result
from guet.commit import PostCommitManager


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
