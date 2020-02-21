import unittest
from unittest.mock import patch

from guet.git.git_path_from_cwd import git_path_from_cwd


class TestGitPathFromCwd(unittest.TestCase):

    @patch('guet.git.git_path_from_cwd.getcwd')
    def test_git_path_from_cwd_combines_cwd_to_git_path(self, mock_getcwd):
        mock_dir_name = '/path'
        mock_getcwd.return_value = mock_dir_name
        result = git_path_from_cwd()
        self.assertEqual(result, '/path/.git')
