import unittest
from unittest.mock import patch

from guet.git.hook_present import hook_present


class TestHookPresent(unittest.TestCase):
    @patch('guet.git.hook_present.isfile')
    @patch('guet.git.hook_present.join')
    def test_hook_present_returns_true_if_hook_is_present_at_path(self, mock_join, mock_isfile):

        mock_join.side_effect = lambda a, b: a + '/' + b
        mock_isfile.side_effect = lambda path: path == '/Users/user/workspace/guet/.git', 'pre-commit'
        self.assertTrue(hook_present('/Users/user/workspace/guet/.git', 'pre-commit'))
