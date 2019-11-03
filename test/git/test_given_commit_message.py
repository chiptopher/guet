import unittest
from os.path import join
from unittest.mock import patch, mock_open

from guet.git.given_commit_message import given_commit_message


class TestGivenCommitMessage(unittest.TestCase):

    @patch('builtins.open', new_callable=mock_open())
    def test_gets_lines_from_commit_editmsg_file(self,
                                                 mock_open):
        mock_open.return_value.readlines.return_value = [
            'Line1\n',
            'Line2\n'
        ]
        result = given_commit_message('path/to/.git')
        mock_open.assert_called_with(join('path/to/.git', 'COMMIT_EDITMSG'), 'r')

        self.assertEqual(['Line1\n', 'Line2\n'], result)

