import unittest
from os.path import join
from unittest.mock import mock_open, patch

from guet import constants
from guet.config import CONFIGURATION_DIRECTORY
from guet.config.committer import Committer
from guet.config.set_current_committers import set_current_committers


class TestSetCurrentCommitters(unittest.TestCase):

    @patch('guet.config.set_current_committers.read_lines')
    @patch('guet.config.set_current_committers.write_lines')
    @patch('guet.config.set_current_committers.git_path_from_cwd')
    @patch('time.time')
    def test_writes_committer_initials_and_current_time_to_committers_set_file(self,
                                                                               mock_time,
                                                                               mock_git_path,
                                                                               mock_write_lines,
                                                                               mock_read_lines):
        mock_read_lines.return_value = []
        mock_git_path.return_value = '/absolute/path/to/.git'
        mock_time.return_value = 1000000000
        set_current_committers([Committer('name', 'email', 'initials1'), Committer('name', 'email', 'initials2')])

        mock_write_lines.assert_called_with(join(CONFIGURATION_DIRECTORY, constants.COMMITTERS_SET),
                                            ['initials1,initials2,1000000000000,/absolute/path/to/.git\n'])
