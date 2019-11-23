import unittest
from os.path import join

from unittest.mock import patch

from guet import constants
from guet.config import CONFIGURATION_DIRECTORY
from guet.config.committer import Committer
from guet.config.set_author import set_committer_as_author


class TestSetAuthor(unittest.TestCase):

    @patch('builtins.open', new_callable=unittest.mock.mock_open())
    def test_writes_the_committer_name_to_the_author_name_file(self, mock_open):
        committer = Committer('name', 'email', 'initials')
        set_committer_as_author(committer)
        mock_open.assert_any_call(join(CONFIGURATION_DIRECTORY, constants.AUTHOR_NAME), 'w')
        mock_open.return_value.write.assert_any_call('name\n')

    @patch('builtins.open', new_callable=unittest.mock.mock_open())
    def test_writes_the_commiter_email_to_the_author_email_file(self, mock_open):
        committer = Committer('name', 'email', 'initials')
        set_committer_as_author(committer)
        mock_open.return_value.write.assert_any_call('email\n')
