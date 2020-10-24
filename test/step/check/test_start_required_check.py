import unittest
from unittest.mock import patch
from pathlib import Path
from guet.steps.check.start_required_check import StartRequiredCheck
from guet.git.git import Git


class TestStartRequiredCheck(unittest.TestCase):

    @patch('guet.steps.check.start_required_check.Git')
    def test_should_stop_returns_true_if_there_are_no_guet_hooks(self, mock_Git):
        path = Path('path/to/project/root')
        check = StartRequiredCheck(path)

        git_instance: Git = mock_Git.return_value
        git_instance.hooks_present = lambda: False

        self.assertTrue(check.should_stop([]))

    @patch('guet.steps.check.start_required_check.Git')
    def test_should_stops_returns_false_when_there_are_guet_hooks(self, mock_Git):
        path = Path('path/to/project/root')
        check = StartRequiredCheck(path)

        git_instance: Git = mock_Git.return_value
        git_instance.hooks_present = lambda: True

        self.assertFalse(check.should_stop([]))

    @patch('guet.steps.check.start_required_check.Git')
    def test_should_stops_checks_git_from_git_root(self, mock_Git):
        path = Path('path/to/project/root')
        check = StartRequiredCheck(path)

        check.should_stop([])

        mock_Git.assert_called_with(path.joinpath('.git'))
