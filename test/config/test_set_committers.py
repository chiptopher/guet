import unittest
from os.path import join
from unittest.mock import patch, call

from guet import constants
from guet.config.set_committers import CommitterInput, set_committers
from test.config import app_config_directory_path


class TestSetCommitters(unittest.TestCase):

    @patch('builtins.open', new_callable=unittest.mock.mock_open())
    def test_writes_to_file_committer_name_and_email(self, mock_open):
        set_committers([CommitterInput('name1', 'email1'), CommitterInput('name2', 'email2')])
        mock_open.assert_called_with(join(app_config_directory_path, constants.COMMITTER_NAMES), 'w')
        self.assertEqual(mock_open.return_value.write.call_args_list[0], call('name1 <email1>\n'))
        self.assertEqual(mock_open.return_value.write.call_args_list[1], call('name2 <email2>\n'))
