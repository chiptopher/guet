import unittest
from unittest.mock import patch

from guet.config.committer import Committer
from guet.hooks.commit_msg import commit_msg


@patch('guet.hooks.commit_msg.git_path_from_cwd')
@patch('guet.hooks.commit_msg.get_current_committers')
@patch('guet.hooks.commit_msg.Git')
class TestCommitMsg(unittest.TestCase):

    def test_adds_committer_names_and_email_to_edit_commitmsg_file(self,
                                                                   mock_git,
                                                                   mock_get_current_committers,
                                                                   mock_git_path_from_cwd):
        mock_git_path_from_cwd.return_value = 'path/to/.git'
        mock_get_current_committers.return_value = [
            Committer('name1', 'email1', 'initials1'),
            Committer('name2', 'email2', 'initials2'),
        ]
        git = mock_git.return_value
        git.commit_msg = [
            'Text\n'
        ]
        commit_msg()
        expected = [
            'Text\n', '\n', 'Co-authored-by: name1 <email1>\n', 'Co-authored-by: name2 <email2>\n'
        ]
        self.assertListEqual(expected, git.commit_msg)

    def test_replaces_co_authored_with_new_committers_if_already_present(self,
                                                                         mock_git,
                                                                         mock_get_current_committers,
                                                                         mock_git_path_from_cwd):
        mock_git_path_from_cwd.return_value = 'path/to/.git'
        mock_get_current_committers.return_value = [
            Committer('name3', 'email3', 'initials3'),
            Committer('name4', 'email4', 'initials4'),
        ]
        git = mock_git.return_value
        git.commit_msg = [
            'Text\n',
            '\n',
            'Co-authored-by: name1 <email1>\n',
            'Co-authored-by: name2 <email2>\n'
        ]
        commit_msg()
        expected = [
            'Text\n', '\n', 'Co-authored-by: name3 <email3>\n', 'Co-authored-by: name4 <email4>\n'
        ]
        self.assertListEqual(expected, git.commit_msg)
