import unittest
from unittest.mock import patch

from guet.config.committer import Committer
from guet.hooks.commit_msg import commit_msg


@patch('guet.hooks.commit_msg.get_current_committers')
@patch('guet.hooks.commit_msg.edit_commit_msg')
class TestCommitMsg(unittest.TestCase):

    def test_adds_committer_names_and_email_to_edit_commitmsg_file(self,
                                                                   mock_edit_commit_msg,
                                                                   mock_get_current_committers):
        mock_get_current_committers.return_value = [
            Committer('name1', 'email1', 'initials1'),
            Committer('name2', 'email2', 'initials2'),
        ]
        commit_msg()
        mock_edit_commit_msg.assert_called_with([
            'Co-authored by: name1 <email1>\n', 'Co-authored by: name2 <email2>\n'
        ])
