import unittest
from pathlib import Path
from unittest.mock import patch
from guet.steps.preparation.local import LocalPreparation


class TestLocalPreparation(unittest.TestCase):

    @patch('guet.steps.preparation.local.isdir')
    @patch('guet.steps.preparation.local.mkdir')
    def test_execute_creates_local_folder_in_repository(self, mock_mkdir, mock_isdir):
        mock_isdir.return_value = False
        path = Path('/path/to/root/directory/')
        preparation = LocalPreparation(path)

        preparation.prepare([])

        mock_mkdir.assert_called_with(path.joinpath('.guet'))

    @patch('guet.steps.preparation.local.isdir')
    @patch('guet.steps.preparation.local.mkdir')
    def test_execute_does_not_create_directory_if_already_present(self, mock_mkdir, mock_isdir):
        mock_isdir.return_value = True
        path = Path('/path/to/root/directory/')
        path = Path('/path/to/root/directory/')
        preparation = LocalPreparation(path)

        preparation.prepare([])

        mock_mkdir.assert_not_called()
