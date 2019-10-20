import unittest
from unittest.mock import patch, MagicMock

from guet.git.set_author import configure_git_author


@patch('guet.git.set_author.subprocess.Popen')
class SetAuthorTest(unittest.TestCase):

    def test_should_open_subprocess_to_set_user_name(self, mock_subprocess_popen):
        configure_git_author('name', 'email')
        mock_subprocess_popen.assert_any_call(['git', 'config', 'user.name', 'name'])
        mock_subprocess_popen.return_value.wait.assert_called()

    def test_should_open_subprocess_to_set_user_email(self, mock_subprocess_popen):
        configure_git_author('name', 'email')
        mock_subprocess_popen.assert_any_call(['git', 'config', 'user.email', 'email'])
        mock_subprocess_popen.return_value.wait.assert_called()
