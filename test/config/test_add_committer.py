import unittest
from os.path import join
from unittest.mock import patch

from guet import constants
from guet.config.add_committer import add_committer
from test.config import app_config_directory_path


class AddCommitterTest(unittest.TestCase):

    @patch('builtins.open', new_callable=unittest.mock.mock_open())
    def test_reads_all_contents_from_committers_file_and_overwrites_it_with_committer_added(self, mock_open):
        mock_open.return_value.readlines.return_value = [
            'initials1,name1,email1\n',
            'initials2,name2,email2\n'
        ]
        add_committer('initials3', 'name3', 'email3')
        mock_open.assert_any_call(join(app_config_directory_path, constants.COMMITTERS), 'r')
        mock_open.assert_any_call(join(app_config_directory_path, constants.COMMITTERS), 'w+')
        mock_open.return_value.writelines.assert_called_with([
            'initials1,name1,email1\n',
            'initials2,name2,email2\n',
            'initials3,name3,email3\n',
        ])

    @patch('builtins.open', new_callable=unittest.mock.mock_open())
    def test_replaces_committer_if_initials_are_alread_in_committers_file(self, mock_open):
        mock_open.return_value.readlines.return_value = [
            'initials1,name1,email1\n',
            'initials2,name2,email2\n',
            'initials3,name3,email3\n'
        ]
        add_committer('initials2', 'new name2', 'new email2')
        mock_open.return_value.writelines.assert_called_with([
            'initials1,name1,email1\n',
            'initials2,new name2,new email2\n',
            'initials3,name3,email3\n'
        ])

