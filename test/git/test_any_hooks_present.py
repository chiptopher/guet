
import unittest
from unittest.mock import patch

from guet.git.any_hooks_present import any_hooks_present


class TestAnyHooksPresent(unittest.TestCase):

    @patch('guet.git.any_hooks_present.hook_present')
    def test_any_hooks_present_checks_if_any_guet_required_hooks_are_present(self, mock_hook_present):
        git_path = '/Users/user/workspace/project/.git'
        hooks = ['pre-commit', 'post-commit', 'commit-msg']

        def _side_effect(_git_path: str, hook_name: str):
            return _git_path == git_path and hook_name in hooks

        mock_hook_present.side_effect = _side_effect

        self.assertTrue(any_hooks_present(git_path))

    @patch('guet.git.any_hooks_present.hook_present')
    def test_any_hooks_present_returns_true_if_any_off_the_hooks_are_present(self, mock_hook_present):
        git_path = '/Users/user/workspace/project/.git'

        mock_hook_present.side_effect = lambda _, hook_name: hook_name == 'pre-commit'
        self.assertTrue(any_hooks_present(git_path))

        mock_hook_present.side_effect = lambda _, hook_name: hook_name == 'post-commit'
        self.assertTrue(any_hooks_present(git_path))

        mock_hook_present.side_effect = lambda _, hook_name: hook_name == 'commit-msg'
        self.assertTrue(any_hooks_present(git_path))
