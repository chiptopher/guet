import unittest
from unittest.mock import patch

from guet.config.committer import Committer
from guet.hooks.commit_msg import commit_msg


@patch('guet.hooks.commit_msg.given_commit_message')
@patch('guet.hooks.commit_msg.git_path_from_cwd')
@patch('guet.hooks.commit_msg.get_current_committers')
@patch('guet.hooks.commit_msg.edit_commit_msg')
class TestCommitMsg(unittest.TestCase):

    def test_adds_committer_names_and_email_to_edit_commitmsg_file(self,
                                                                   mock_edit_commit_msg,
                                                                   mock_get_current_committers,
                                                                   mock_git_path_from_cwd,
                                                                   mock_given_commit_message):
        mock_git_path_from_cwd.return_value = 'path/to/.git'
        mock_get_current_committers.return_value = [
            Committer('name1', 'email1', 'initials1'),
            Committer('name2', 'email2', 'initials2'),
        ]
        mock_given_commit_message.return_value = [
            'Text\n'
        ]
        commit_msg()
        mock_edit_commit_msg.assert_called_with('path/to/.git', [
            'Text\n', '\n', 'Co-authored-by: name1 <email1>\n', 'Co-authored-by: name2 <email2>\n'
        ])

    def test_replaces_co_authored_with_new_committers_if_already_present(self,
                                                                         mock_edit_commit_msg,
                                                                         mock_get_current_committers,
                                                                         mock_git_path_from_cwd,
                                                                         mock_given_commit_message):
        mock_git_path_from_cwd.return_value = 'path/to/.git'
        mock_get_current_committers.return_value = [
            Committer('name3', 'email3', 'initials3'),
            Committer('name4', 'email4', 'initials4'),
        ]
        mock_given_commit_message.return_value = [
            'Text\n',
            '\n',
            'Co-authored-by: name1 <email1>\n',
            'Co-authored-by: name2 <email2>\n'
        ]
        commit_msg()
        mock_edit_commit_msg.assert_called_with('path/to/.git', [
            'Text\n', '\n', 'Co-authored-by: name3 <email3>\n', 'Co-authored-by: name4 <email4>\n'
        ])
