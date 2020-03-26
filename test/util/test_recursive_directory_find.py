from os.path import join
from pathlib import Path
from unittest import TestCase
from unittest.mock import patch, Mock

from guet.util import recursive_directory_find


@patch('guet.util._recursive_directory_find.expanduser', return_value='/Users/name')
@patch('guet.util._recursive_directory_find.Path')
class TestRecursiveDirectoryFind(TestCase):

    def test_returns_given_path_if_contains_desired_directory(self, mock_path, mock_is_mount):
        joined_with_git = Mock()
        joined_with_git.is_dir.return_value = True
        joined_with_git.__str__ = Mock()
        joined_with_git.__str__.return_value = join('.', '.git')

        given_mock_path = Mock()
        given_mock_path.joinpath.return_value = joined_with_git

        mock_path.side_effect = [given_mock_path]

        result = recursive_directory_find('.', '.git')
        self.assertEqual(join('.', '.git'), result)

    def test_checks_parent_directory_for_desired_directory(self, mock_path, mock_is_mount):
        parent_joined_with_git = Mock()
        parent_joined_with_git.is_dir.return_value = True
        parent_joined_with_git.__str__ = Mock()
        parent_joined_with_git.__str__.return_value = join('.', '.git')

        parent = Mock()
        parent.joinpath.return_value = parent_joined_with_git

        joined_with_git = Mock()

        joined_with_git.is_dir.return_value = False

        given_mock_path = Mock()
        given_mock_path.joinpath.return_value = joined_with_git
        given_mock_path.parent = parent

        mock_path.side_effect = [given_mock_path]

        result = recursive_directory_find('./path', '.git')
        self.assertEqual(join('.', '.git'), result)

    def test_raises_exception_if_mount_is_found(self, mock_path, mock_expanduser):
        parent: Path = Mock()
        parent.__str__ = Mock()
        parent.__str__.return_value = '/Users/name'

        joined_with_git = Mock()

        joined_with_git.is_dir.return_value = False

        given_mock_path = Mock()
        given_mock_path.joinpath.return_value = joined_with_git
        given_mock_path.parent = parent

        mock_path.side_effect = [given_mock_path]

        try:
            recursive_directory_find('/path', '.git')
            self.fail('Should raise exception')
        except FileNotFoundError:
            pass
