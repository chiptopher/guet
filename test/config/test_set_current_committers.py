import unittest
from os.path import join
from unittest.mock import mock_open, patch

from guet import constants
from guet.config import CONFIGURATION_DIRECTORY
from guet.config.committer import Committer
from guet.config.set_current_committers import set_current_committers


class TestSetCurrentCommitters(unittest.TestCase):

    @patch('time.time')
    @patch('builtins.open', new_callable=mock_open())
    def test_writes_committer_initials_and_current_time_to_committers_set_file(self,
                                                                               mock_open,
                                                                               mock_time):
        mock_time.return_value = 1000000000
        set_current_committers([Committer('name', 'email', 'initials1'), Committer('name', 'email', 'initials2')])
        mock_open.assert_called_with(join(CONFIGURATION_DIRECTORY, constants.COMMITTERS_SET), 'w')
        mock_open.return_value.write.assert_called_with('initials1,initials2,1000000000000\n')
