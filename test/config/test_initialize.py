import unittest
from pathlib import Path
from unittest.mock import patch

from os.path import expanduser, join

from guet import constants, __version__
from guet.config.initialize import initialize

from test.config import app_config_directory_path


@patch('guet.config.initialize.write_lines')
@patch('guet.config.initialize.mkdir')
class TestInitialize(unittest.TestCase):

    def test_creates_app_configuration_folder_in_user_home_directory_if_it_does_not_exist(self,
                                                                                          mock_mkdir,
                                                                                          mock_write_lines):
        initialize()
        mock_mkdir.assert_any_call(app_config_directory_path)

    def test_creates_file_for_current_committer_names(self, mock_mkdir, mock_write_lines):
        initialize()
        mock_write_lines.assert_any_call(Path(join(app_config_directory_path, constants.COMMITTER_NAMES)), [])

    def test_creates_file_for_commiters_names(self, mock_mkdir, mock_write_lines):
        initialize()
        mock_write_lines.assert_any_call(Path(join(app_config_directory_path, constants.COMMITTERS)), [])

    def test_creates_file_for_configuration(self, mock_mkdir, mock_write_lines):
        initialize()
        mock_write_lines.assert_any_call(Path(join(app_config_directory_path, constants.CONFIG)), [])

    def test_creates_file_for_committers_set(self, mock_mkdir, mock_write_lines):
        initialize()
        mock_write_lines.assert_any_call(Path(join(app_config_directory_path, constants.COMMITTERS_SET)), [])

    def test_writes_version_number_to_config_file(self, mock_mkdir, mock_write_lines):
        initialize()
        mock_write_lines.assert_called_with(Path(join(app_config_directory_path, constants.CONFIG)),
                                            [f'{__version__}\n', '\n'])
