import unittest
from unittest.mock import patch, mock_open

from guet.config.most_recent_committers_set import most_recent_committers_set
from guet.config.errors import PairSetError


@patch('guet.config.most_recent_committers_set.git_path_from_cwd', return_value='/path/to/.git')
@patch('guet.config.most_recent_committers_set.read_lines')
class TestMostRecentCommittersSet(unittest.TestCase):

    def test_gets_the_timestamp_from_committers_set(self,
                                                    mock_read_lines,
                                                    mock_git_cwd):
        mock_read_lines.return_value = ['initials1,initials2,1000000000,/path/to/.git']
        result = most_recent_committers_set()
        self.assertEqual(1000000000, result)

    def test_raises_exception_when_no_committersset_have_path_to_git(self,
                                                                     mock_read_lines,
                                                                     mock_git_cwd):
        mock_read_lines.return_value = ['initials1,initials2,1000000000']
        try:
            result = most_recent_committers_set()
            self.fail(f'Should raise {PairSetError.__name__}')
        except PairSetError:
            pass
