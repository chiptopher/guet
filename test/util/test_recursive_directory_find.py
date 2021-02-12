from pathlib import Path
from unittest import TestCase
from unittest.mock import Mock, patch

from guet.util import recursive_directory_find


@patch('guet.util._recursive_directory_find.expanduser', return_value='/Users/name')
@patch('guet.util._recursive_directory_find.Path')
class TestRecursiveDirectoryFind(TestCase):

    def test_returns_given_path_if_contains_desired_directory(self, mock_path, mock_is_mount):
        joined_with_git = Mock()
        joined_with_git.is_dir.return_value = True

        given_mock_path = Mock()
        given_mock_path.joinpath.return_value = joined_with_git
        given_mock_path.__str__ = Mock()
        given_mock_path.__str__.return_value = '.'

        result = recursive_directory_find(given_mock_path, '.git')
        self.assertEqual(given_mock_path, result)

    def test_checks_parent_directory_for_desired_directory(self, mock_path, mock_is_mount):
        parent_joined_with_git = Mock()
        parent_joined_with_git.is_dir.return_value = True

        parent = Mock()
        parent.joinpath.return_value = parent_joined_with_git

        joined_with_git = Mock()

        joined_with_git.is_dir.return_value = False

        given_mock_path = Mock()
        given_mock_path.joinpath.return_value = joined_with_git
        given_mock_path.parent = parent

        result = recursive_directory_find(given_mock_path, '.git')
        self.assertEqual(parent, result)

    def test_raises_exception_if_mount_is_found(self, mock_path, mock_expanduser):
        parent: Path = Mock()
        parent.__str__ = Mock()
        parent.__str__.return_value = '/Users/name'

        joined_with_git = Mock()

        joined_with_git.is_dir.return_value = False

        given_mock_path = Mock()
        given_mock_path.joinpath.return_value = joined_with_git
        given_mock_path.parent = parent

        try:
            recursive_directory_find(given_mock_path, '.git')
            self.fail('Should raise exception')
        except FileNotFoundError:
            pass
