import unittest
from unittest.mock import patch, mock_open

from guet.config.most_recent_committers_set import most_recent_committers_set


@patch('guet.config.most_recent_committers_set.read_lines')
class TestMostRecentCommittersSet(unittest.TestCase):

    def test_gets_the_timestamp_from_committers_set(self,
                                                    mock_read_lines):
        mock_read_lines.return_value = ['initials1,initials2,1000000000']
        result = most_recent_committers_set()
        self.assertEqual(1000000000, result)
