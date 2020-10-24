import unittest
from unittest.mock import Mock, call, patch
from pathlib import Path

from guet.config import CONFIGURATION_DIRECTORY
from guet.steps.preparation.initialize import InitializePreparation
from guet.files import FileSystem
from guet import constants


@patch('guet.steps.preparation.initialize.mkdir')
class TestInitializePreparation(unittest.TestCase):

    def test_prepare_creates_initialization_folders_and_files(self, mock_mkdir):
        config_dir = Path(CONFIGURATION_DIRECTORY)
        mock_filesystem: FileSystem = Mock()
        preparation_step = InitializePreparation(mock_filesystem)
        preparation_step.prepare([])

        mock_filesystem.get.assert_has_calls([
            call(Path(config_dir.joinpath(constants.COMMITTER_NAMES))),
            call().read(),
            call(Path(config_dir.joinpath(constants.COMMITTERS))),
            call().read(),
            call(Path(config_dir.joinpath(constants.COMMITTERS_SET))),
            call().read(),
            call(Path(config_dir.joinpath(constants.ERRORS))),
            call().read(),
        ])

        mock_filesystem.save_all.assert_called()

    def test_prepare_creates_initialization_directory(self, mock_mkdir):
        config_dir = Path(CONFIGURATION_DIRECTORY)
        mock_filesystem: FileSystem = Mock()
        preparation_step = InitializePreparation(mock_filesystem)
        preparation_step.prepare([])

        mock_mkdir.assert_called_with(CONFIGURATION_DIRECTORY)

