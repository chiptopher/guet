import unittest
from unittest.mock import patch

from guet.util import project_root


@patch('guet.util._project_root.getcwd')
@patch('guet.util._project_root.recursive_directory_find')
class TestProjectRoot(unittest.TestCase):
    def test_finds_folder_with_git_from_given_directory(self, mock_recursive_directory_find, mock_getcwd):
        result = project_root()
        self.assertEqual(result, mock_recursive_directory_find.return_value)
        mock_recursive_directory_find.assert_called_with(mock_getcwd.return_value, '.git')
