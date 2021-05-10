import unittest
from pathlib import Path
from unittest.mock import Mock, call, patch

from guet import constants
from guet.config import CONFIGURATION_DIRECTORY
from guet.files import FileSystem
from guet.steps.preparation.initialize import InitializePreparation


@patch('guet.steps.preparation.initialize.mkdir')
@patch('guet.steps.preparation.initialize.isdir')
class TestInitializePreparation(unittest.TestCase):

    def test_prepare_creates_initialization_folders_and_files(self,
                                                              mock_isdir,
                                                              _1):
        mock_isdir.return_value = False
        config_dir = Path(CONFIGURATION_DIRECTORY)
        mock_filesystem: FileSystem = Mock()
        preparation_step = InitializePreparation(mock_filesystem)
        preparation_step.prepare([])

        mock_filesystem.get.assert_has_calls([
            call(Path(config_dir.joinpath(constants.COMMITTER_NAMES))),
            call().write([]),
            call(Path(config_dir.joinpath(constants.CONFIG))),
            call().write([]),
            call(Path(config_dir.joinpath(constants.COMMITTERS))),
            call().write([]),
            call(Path(config_dir.joinpath(constants.COMMITTERS_SET))),
            call().write([]),
            call(Path(config_dir.joinpath(constants.ERRORS))),
            call().write([]),
        ])

        mock_filesystem.save_all.assert_called()

    def test_prepare_creates_initialization_directory(self, mock_isdir, mock_mkdir):
        mock_isdir.return_value = False
        mock_filesystem: FileSystem = Mock()
        preparation_step = InitializePreparation(mock_filesystem)
        preparation_step.prepare([])

        mock_mkdir.assert_called_with(CONFIGURATION_DIRECTORY)

    def test_prepare_doesnt_create_initialization_directory_if_already_present(self,
                                                                               mock_isdir,
                                                                               mock_mkdir):
        mock_isdir.return_value = True
        mock_filesystem: FileSystem = Mock()
        preparation_step = InitializePreparation(mock_filesystem)
        preparation_step.prepare([])

        mock_mkdir.assert_not_called()
