import unittest
from unittest.mock import patch, mock_open

from guet.config.most_recent_committers_set import most_recent_committers_set


@patch('builtins.open', new_callable=mock_open())
class TestMostRecentCommittersSet(unittest.TestCase):

    def test_gets_the_timestamp_from_committers_set(self,
                                                    mock_open):

        mock_open.return_value.readline.return_value = 'initials1,initials2,1000000000\n'
        result = most_recent_committers_set()
        self.assertEqual(1000000000, result)
