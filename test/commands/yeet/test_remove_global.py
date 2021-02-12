from pathlib import Path
from unittest import TestCase
from unittest.mock import patch

from guet.commands.yeet._remove_global import RemoveGlobal
from guet.config import CONFIGURATION_DIRECTORY


@patch('builtins.print')
@patch('guet.commands.yeet._remove_global.rmtree')
class TestRemoveGlobal(TestCase):
    def test_removes_guet_directory_with_dash_f(self, mock_rmtree, mock_print):
        remove_global = RemoveGlobal()
        remove_global.execute(['-f'])

        mock_rmtree.assert_called_with(Path(CONFIGURATION_DIRECTORY))
        mock_print.assert_called_with('Bye!')

    def test_removes_guet_directory_with_force(self, mock_rmtree, mock_print):
        remove_global = RemoveGlobal()
        remove_global.execute(['--force'])

        mock_rmtree.assert_called_with(Path(CONFIGURATION_DIRECTORY))
        mock_print.assert_called_with('Bye!')

    def test_doesnt_remove_without_force(self, mock_rmtree, mock_print):
        remove_global = RemoveGlobal()
        remove_global.execute(['--other'])

        mock_rmtree.assert_not_called()
        mock_print.assert_not_called()
