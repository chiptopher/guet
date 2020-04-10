import unittest
from os.path import join
from unittest.mock import patch

from guet import constants
from guet.config import CONFIGURATION_DIRECTORY
from guet.committers.committer import Committer
from guet.committers._set_current_committers import set_current_committers


class TestSetCurrentCommitters(unittest.TestCase):

    @patch('guet.committers._set_current_committers.read_lines')
    @patch('guet.committers._set_current_committers.write_lines')
    @patch('time.time')
    def test_writes_committer_initials_and_current_time_to_committers_set_file(self,
                                                                               mock_time,
                                                                               mock_write_lines,
                                                                               mock_read_lines):
        mock_read_lines.return_value = []
        mock_time.return_value = 1000000000
        set_current_committers([Committer('name', 'email', 'initials1'), Committer('name', 'email', 'initials2')],
                               '/path/to/project/.git')

        mock_write_lines.assert_called_with(join(CONFIGURATION_DIRECTORY, constants.COMMITTERS_SET),
                                            ['initials1,initials2,1000000000000,/path/to/project/.git'])

    @patch('guet.committers._set_current_committers.read_lines')
    @patch('guet.committers._set_current_committers.write_lines')
    @patch('time.time')
    def test_adds_given_committer_initials_to_committers_set_file(self,
                                                                  mock_time,
                                                                  mock_write_lines,
                                                                  mock_read_lines):
        mock_read_lines.return_value = [
            'initials3,initials4,1000000000000,/absolute/path/to/other/.git',
        ]
        mock_time.return_value = 1000000000
        set_current_committers([Committer('name', 'email', 'initials1'), Committer('name', 'email', 'initials2')],
                               '/path/to/project/.git')
        lines = [
            'initials3,initials4,1000000000000,/absolute/path/to/other/.git',
            'initials1,initials2,1000000000000,/path/to/project/.git'
        ]
        mock_write_lines.assert_called_with(join(CONFIGURATION_DIRECTORY, constants.COMMITTERS_SET), lines)

    @patch('guet.committers._set_current_committers.read_lines')
    @patch('guet.committers._set_current_committers.write_lines')
    @patch('time.time')
    def test_overwrites_set_initials_if_git_path_matches(self,
                                                         mock_time,
                                                         mock_write_lines,
                                                         mock_read_lines):
        mock_read_lines.return_value = [
            'initials1,initials2,1000000,/path/to/project/.git',
        ]
        mock_time.return_value = 1000000000
        set_current_committers([Committer('name', 'email', 'initials3'), Committer('name', 'email', 'initials4')],
                               '/path/to/project/.git')

        lines = [
            'initials3,initials4,1000000000000,/path/to/project/.git'
        ]
        mock_write_lines.assert_called_with(join(CONFIGURATION_DIRECTORY, constants.COMMITTERS_SET), lines)
