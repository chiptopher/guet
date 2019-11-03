import unittest
from os.path import join
from unittest.mock import patch, mock_open

from guet.git.edit_commit_msg import edit_commit_msg


class TestEditCommitMsg(unittest.TestCase):

    @patch('builtins.open', new_callable=mock_open())
    def test_writes_text_to_edit_commit_msg_file(self,
                                                 mock_open):
        edit_commit_msg('path/to/.git', [
            'Text\n'
        ])

        mock_open.assert_called_with(join('path/to/.git', 'COMMIT_EDITMSG'), 'w')
        mock_open.return_value.writelines.assert_called_with(['Text\n'])
