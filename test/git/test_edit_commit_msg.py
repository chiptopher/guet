import unittest
from os.path import join
from unittest.mock import patch, mock_open

from guet.git.edit_commit_msg import edit_commit_msg


class TestEditCommitMsg(unittest.TestCase):

    @patch('builtins.open', new_callable=mock_open())
    def test_appends_given_text_to_file(self, mock_open):
        git_path = 'path/to/.git'
        edit_commit_msg(git_path, ['line1\n', 'line2\n'])
        mock_open.assert_called_with(join(git_path, 'COMMIT_EDITMSG'), 'a')
        mock_open.return_value.writelines.assert_called_with(['line1\n', 'line2\n'])
