import unittest
from unittest.mock import patch

from guet.config import CONFIGURATION_DIRECTORY
from guet.config.already_initialized import already_initialized


class TestAlreadyInitialized(unittest.TestCase):
    @patch('guet.config.already_initialized.isdir')
    def test_returns_true_if_config_folder_already_exists(self, mock_is_dir):
        mock_is_dir.side_effect = lambda path: path == CONFIGURATION_DIRECTORY
        self.assertTrue(already_initialized())

