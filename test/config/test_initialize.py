import unittest
from unittest.mock import patch

from os.path import expanduser, join

from guet import constants
from guet.config.initialize import initialize

from test.config import app_config_directory_path


@patch('guet.config.initialize.mkdir')
class TestInitialize(unittest.TestCase):

    @patch('builtins.open', new_callable=unittest.mock.mock_open())
    def test_creates_app_configuration_folder_in_user_home_directory_if_it_does_not_exist(self,
                                                                                          mock_open,
                                                                                          mock_mkdir):
        initialize()
        mock_mkdir.assert_any_call(app_config_directory_path)


    @patch('builtins.open', new_callable=unittest.mock.mock_open())
    def test_creates_file_for_current_committer_names(self, mock_open, mock_mkdir):
        initialize()
        mock_open.assert_any_call(join(app_config_directory_path, constants.COMMITTER_NAMES), 'w')

    @patch('builtins.open', new_callable=unittest.mock.mock_open())
    def test_creates_file_for_current_author_email(self, mock_open, mock_mkdir):
        initialize()
        mock_open.assert_any_call(join(app_config_directory_path, constants.AUTHOR_EMAIL), 'w')

    @patch('builtins.open', new_callable=unittest.mock.mock_open())
    def test_creates_file_for_current_author_name(self, mock_open, mock_mkdir):
        initialize()
        mock_open.assert_any_call(join(app_config_directory_path, constants.AUTHOR_NAME), 'w')

    @patch('builtins.open', new_callable=unittest.mock.mock_open())
    def test_creates_file_for_commiters_names(self, mock_open, mock_mkdir):
        initialize()
        mock_open.assert_any_call(join(app_config_directory_path, constants.COMMITTERS), 'w')

    @patch('builtins.open', new_callable=unittest.mock.mock_open())
    def test_creates_file_for_committers_set(self, mock_open, mock_mkdir):
        initialize()
        mock_open.assert_any_call(join(app_config_directory_path, constants.COMMITTERS_SET), 'w')
