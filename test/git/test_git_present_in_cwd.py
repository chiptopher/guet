import unittest
from unittest.mock import patch

from guet.git.git_present_in_cwd import git_present_in_cwd


class TestGitPresentInCwd(unittest.TestCase):

    @patch('guet.git.git_present_in_cwd.getcwd')
    @patch('guet.git.git_present_in_cwd.isdir')
    def test_git_path_from_cwd_combines_cwd_to_git_path(self, mock_isdir, mock_getcwd):
        mock_dir_name = '/path'
        mock_getcwd.return_value = mock_dir_name
        mock_isdir.side_effect = lambda dir_name: dir_name == mock_dir_name + '/.git'
        self.assertTrue(git_present_in_cwd())
