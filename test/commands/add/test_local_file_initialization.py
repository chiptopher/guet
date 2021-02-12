import unittest
from pathlib import Path
from unittest.mock import Mock, call, patch

from guet import constants
from guet.commands.add._local_file_initialization import \
    LocalFilesInitialization
from guet.config import CONFIGURATION_DIRECTORY
from guet.files import FileSystem


@patch('guet.commands.add._local_file_initialization.project_root', return_value='path/to/project/root')
@patch('guet.commands.add._local_file_initialization.mkdir')
@patch('guet.commands.add._local_file_initialization.isdir')
class TestInitializePreparation(unittest.TestCase):

    def test_prepare_creates_initialization_folders_and_files(self, mock_isdir, mock_mkdir, mock_project_root):
        mock_isdir.return_value = False
        mock_project_root.return_value = 'path'
        config_dir = Path(mock_project_root()).joinpath('.guet')

        mock_filesystem: FileSystem = Mock()
        preparation_step = LocalFilesInitialization(mock_filesystem, Mock())
        preparation_step.prepare(['--local'])

        mock_filesystem.get.assert_has_calls([
            call(Path(config_dir.joinpath('committers'))),
            call().read(),
        ])

        mock_filesystem.save_all.assert_called()

    def test_prepare_creates_initialization_directory(self, mock_isdir, mock_mkdir, mock_project_root):
        mock_isdir.return_value = False
        config_dir = Path(mock_project_root()).joinpath('.guet')

        mock_filesystem: FileSystem = Mock()
        preparation_step = LocalFilesInitialization(mock_filesystem, Mock())
        preparation_step.prepare(['--local'])

        mock_mkdir.assert_called_with(config_dir)

    def test_prepare_doesnt_create_initialization_directory_if_already_present(self, mock_isdir, mock_mkdir, mock_project_root):
        mock_isdir.return_value = True

        mock_filesystem: FileSystem = Mock()
        preparation_step = LocalFilesInitialization(mock_filesystem, Mock())
        preparation_step.prepare(['--local'])

        mock_mkdir.assert_not_called()

    def test_prepare_swaps_committers_to_local(self, mock_isdir, mock_mkdir, mock_project_root):
        mock_isdir.return_value = True

        mock_filesystem: FileSystem = Mock()
        mock_committers = Mock()
        preparation_step = LocalFilesInitialization(mock_filesystem, mock_committers)
        preparation_step.prepare(['--local'])

        mock_committers.to_local.assert_called()
