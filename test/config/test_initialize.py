import unittest
from unittest.mock import patch

from os.path import expanduser, join

from guet import constants
from guet.config.initialize import initialize

from test.config import app_config_directory_path


@patch('guet.config.initialize.sqlite3.connect')
@patch('guet.config.initialize.mkdir')
class TestInitialize(unittest.TestCase):

    @patch('builtins.open', new_callable=unittest.mock.mock_open())
    def test_creates_app_configuration_folder_in_user_home_directory_if_it_does_not_exist(self,
                                                                                          mock_open,
                                                                                          mock_mkdir,
                                                                                          mock_connect):
        initialize()
        mock_mkdir.assert_any_call(app_config_directory_path)

    @patch('builtins.open', new_callable=unittest.mock.mock_open())
    def test_connects_to_datasource_file_in_configuration_folder_to_create_it(self,
                                                                              mock_open,
                                                                              mock_mkdir,
                                                                              mock_connect):
        initialize()
        mock_connect.assert_called_with(join(app_config_directory_path, constants.DATA_SOURCE_NAME))

    @patch('builtins.open', new_callable=unittest.mock.mock_open())
    def test_creates_committer_table(self, mock_open, mock_mkdir, mock_connect):
        initialize()
        create_query = """CREATE TABLE committer
                              (initials TEXT NOT NULL PRIMARY KEY,
                               name TEXT NOT NULL,
                               email TEXT NOT NULL)"""
        mock_connect.return_value.execute.assert_any_call(create_query)

    @patch('builtins.open', new_callable=unittest.mock.mock_open())
    def test_creates_pair_set_table(self, mock_open, mock_mkdir, mock_connect):
        initialize()
        create_query = """CREATE TABLE pair_set
                              (id INTEGER NOT NULL PRIMARY KEY,
                              set_time INTEGER NOT NULL)
                              """
        mock_connect.return_value.execute.assert_any_call(create_query)

    @patch('builtins.open', new_callable=unittest.mock.mock_open())
    def test_creates_pair_set_committer_table(self, mock_open, mock_mkdir, mock_connect):
        initialize()
        create_query = """CREATE TABLE pair_set_committer
                              (id INTEGER NOT NULL PRIMARY KEY,
                              committer_initials TEXT NOT NULL,
                              pair_set_id INTEGER NOT NULL,
                              FOREIGN KEY (pair_set_id) REFERENCES pair_set(id),
                              FOREIGN KEY (committer_initials) REFERENCES comitter(initials)
                              )
                              """
        mock_connect.return_value.execute.assert_any_call(create_query)

    @patch('builtins.open', new_callable=unittest.mock.mock_open())
    def test_closes_connection(self,
                               mock_open, mock_mkdir, mock_connect):
        initialize()
        mock_connect.return_value.close.assert_called()

    @patch('builtins.open', new_callable=unittest.mock.mock_open())
    def test_creates_file_for_current_committer_names(self, mock_open, mock_mkdir, mock_connect):
        initialize()
        mock_open.assert_any_call(join(app_config_directory_path, constants.COMMITTER_NAMES), 'w')

    @patch('builtins.open', new_callable=unittest.mock.mock_open())
    def test_creates_file_for_current_author_email(self, mock_open, mock_mkdir, mock_connect):
        initialize()
        mock_open.assert_any_call(join(app_config_directory_path, constants.AUTHOR_EMAIL), 'w')

    @patch('builtins.open', new_callable=unittest.mock.mock_open())
    def test_creates_file_for_current_author_name(self, mock_open, mock_mkdir, mock_connect):
        initialize()
        mock_open.assert_any_call(join(app_config_directory_path, constants.AUTHOR_NAME), 'w')

    @patch('builtins.open', new_callable=unittest.mock.mock_open())
    def test_creates_file_for_commiters_names(self, mock_open, mock_mkdir, mock_connect):
        initialize()
        mock_open.assert_any_call(join(app_config_directory_path, constants.COMMITTERS), 'w')
