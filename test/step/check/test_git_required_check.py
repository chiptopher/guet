import unittest
from unittest.mock import patch
from guet.git.errors import NoGitPresentError
from pathlib import Path
from guet.steps.check.git_required_check import GitRequiredCheck


@patch('guet.steps.check.git_required_check.Git')
class TestGitRequiredCheck(unittest.TestCase):
    def test_should_stops_when_git_not_present_in_path(self, mock_git):
        mock_git.side_effect = NoGitPresentError()
        path_to_git_directory = Path()
        check = GitRequiredCheck(path_to_git_directory)

        result = check.should_stop([])

        self.assertTrue(result)
