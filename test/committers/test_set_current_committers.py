import unittest
from os.path import join
from pathlib import Path
from unittest.mock import patch

from guet import constants
from guet.committers._committers_set import CommittersSet
from guet.config import CONFIGURATION_DIRECTORY
from guet.committers.committer import Committer
from guet.committers._set_current_committers import set_current_committers


class TestSetCurrentCommitters(unittest.TestCase):

    @patch('guet.committers._set_current_committers.all_committers_set')
    @patch('guet.committers._set_current_committers.write_lines')
    @patch('time.time')
    def test_writes_committer_initials_and_current_time_to_committers_set_file(self,
                                                                               mock_time,
                                                                               mock_write_lines,
                                                                               all_committers_set):
        all_committers_set.return_value = []
        mock_time.return_value = 1000000000
        set_current_committers([Committer('name', 'email', 'initials1'), Committer('name', 'email', 'initials2')],
                               Path('/path/to/project/.git'))

        formatted_path = str(Path('/path/to/project/.git'))
        mock_write_lines.assert_called_with(Path(join(CONFIGURATION_DIRECTORY, constants.COMMITTERS_SET)),
                                            [f'initials1,initials2,1000000000000,{formatted_path}'])

    @patch('guet.committers._set_current_committers.all_committers_set')
    @patch('guet.committers._set_current_committers.write_lines')
    @patch('time.time')
    def test_adds_given_committer_initials_to_committers_set_file(self,
                                                                  mock_time,
                                                                  mock_write_lines,
                                                                  all_committers_set):
        all_committers_set.return_value = [
            CommittersSet(['initials3', 'initials4'], 1000000000000, Path('/absolute/path/to/other/.git')),
        ]
        mock_time.return_value = 1000000000
        set_current_committers([Committer('name', 'email', 'initials1'), Committer('name', 'email', 'initials2')],
                               Path('/path/to/project/.git'))
        lines = [
            f'initials3,initials4,1000000000000,{str(Path("/absolute/path/to/other/.git"))}',
            f'initials1,initials2,1000000000000,{str(Path("/path/to/project/.git"))}'
        ]
        mock_write_lines.assert_called_with(Path(join(CONFIGURATION_DIRECTORY, constants.COMMITTERS_SET)).absolute(),
                                            lines)

    @patch('guet.committers._set_current_committers.all_committers_set')
    @patch('guet.committers._set_current_committers.write_lines')
    @patch('time.time')
    def test_overwrites_set_initials_if_git_path_matches(self,
                                                         mock_time,
                                                         mock_write_lines,
                                                         all_committers_set):
        all_committers_set.return_value = [
            CommittersSet(['initials1', 'initials2'], 1000000, Path('/path/to/project/.git')),
        ]
        mock_time.return_value = 1000000000
        set_current_committers([Committer('name', 'email', 'initials3'), Committer('name', 'email', 'initials4')],
                               Path('/path/to/project/.git'))

        formatted_path = str(Path('/path/to/project/.git'))
        lines = [
            f'initials3,initials4,1000000000000,{formatted_path}'
        ]
        mock_write_lines.assert_called_with(Path(join(CONFIGURATION_DIRECTORY, constants.COMMITTERS_SET)), lines)
