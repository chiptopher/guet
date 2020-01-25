import unittest
from os.path import join

from unittest.mock import patch

from guet import constants
from guet.config import CONFIGURATION_DIRECTORY
from guet.config.committer import Committer
from guet.config.get_current_committers import get_current_committers


@patch('guet.config.get_current_committers.git_path_from_cwd', return_value='/absolute/path/to/.git')
@patch('guet.config.get_current_committers.get_committers')
@patch('guet.config.get_current_committers.read_lines')
class TestGetCurrentCommitters(unittest.TestCase):

    def test_reads_committers_from_file_and_returns_committers(self,
                                                               mock_read_lines,
                                                               mock_get_committers,
                                                               mock_git_path_from_cwd):
        mock_get_committers.return_value = [
            Committer('name0', 'email0', 'initials0'),
            Committer('name1', 'email1', 'initials1'),
            Committer('name2', 'email2', 'initials2')
        ]
        mock_read_lines.return_value = ['initials1,initials2,1000000000,/absolute/path/to/.git']

        committers = get_current_committers()
        self.assertEqual(committers[0].name, 'name1')
        self.assertEqual(committers[0].email, 'email1')
        self.assertEqual(committers[0].initials, 'initials1')
        self.assertEqual(committers[1].name, 'name2')
        self.assertEqual(committers[1].email, 'email2')
        self.assertEqual(committers[1].initials, 'initials2')

    def test_reads_committers_from_file(self,
                                        mock_read_lines,
                                        mock_get_committers,
                                        mock_git_path_from_cwd):
        mock_read_lines.return_value = ['initials1,initials2,1000000000,/absolute/path/to/.git']
        get_current_committers()
        mock_read_lines.assert_called_with(join(CONFIGURATION_DIRECTORY, constants.COMMITTERS_SET))

    def test_get_current_committers_preserves_order_of_committers(self,
                                                                  mock_read_lines,
                                                                  mock_get_committers,
                                                                  mock_git_path_from_cwd):
        mock_get_committers.return_value = [
            Committer('name0', 'email0', 'initials0'),
            Committer('name1', 'email1', 'initials1'),
            Committer('name2', 'email2', 'initials2')
        ]
        mock_read_lines.return_value = ['initials2,initials1,1000000000,/absolute/path/to/.git']

        committers = get_current_committers()
        self.assertEqual(committers[0].name, 'name2')
        self.assertEqual(committers[0].email, 'email2')
        self.assertEqual(committers[0].initials, 'initials2')
        self.assertEqual(committers[1].name, 'name1')
        self.assertEqual(committers[1].email, 'email1')
        self.assertEqual(committers[1].initials, 'initials1')

    def test_returns_no_committers_if_committerset_file_is_empty(self,
                                                                 mock_read_lines,
                                                                 mock_get_committers,
                                                                 mock_git_path_from_cwd):
        mock_get_committers.return_value = [
            Committer('name0', 'email0', 'initials0'),
            Committer('name1', 'email1', 'initials1'),
            Committer('name2', 'email2', 'initials2')
        ]

        mock_read_lines.return_value = []

        committers = get_current_committers()
        self.assertListEqual([], committers)

    def test_returns_no_committers_if_no_lines_end_with_matching_git_path(self,
                                                                          mock_read_lines,
                                                                          _,
                                                                          mock_git_path_from_cwd):
        mock_read_lines.return_value = [
            'initials1,initials2,1000000000,/project1/.git',
            'initials1,initials2,1000000000,/project2/.git',
        ]

        mock_git_path_from_cwd.return_value = '/project3/.git'

        result = get_current_committers()
        self.assertListEqual([], result)

    def test_returns_committers_that_arent_in_the_first_line(self,
                                                             mock_read_lines,
                                                             mock_get_committers,
                                                             mock_git_path_from_cwd):
        mock_git_path_from_cwd.return_value = '/absolute/path/to/.git'

        mock_get_committers.return_value = [
            Committer('name0', 'email0', 'initials0'),
            Committer('name1', 'email1', 'initials1'),
            Committer('name2', 'email2', 'initials2')
        ]

        mock_read_lines.return_value = [
            'initials0,initials1,1000000000,/absolute/other/path/to/different/.git',
            'initials1,initials2,1000000000,/absolute/path/to/.git',
        ]

        committers = get_current_committers()
        self.assertEqual(committers[0].name, 'name1')
        self.assertEqual(committers[0].email, 'email1')
        self.assertEqual(committers[0].initials, 'initials1')
        self.assertEqual(committers[1].name, 'name2')
        self.assertEqual(committers[1].email, 'email2')
        self.assertEqual(committers[1].initials, 'initials2')
