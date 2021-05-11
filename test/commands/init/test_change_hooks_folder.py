from os import getcwd
from unittest import TestCase
from unittest.mock import Mock, patch

from guet.commands.init._change_hooks_folder import ChangeHooksFolder


@patch('guet.commands.init._change_hooks_folder.Path')
class TestChangeHooksFolder(TestCase):
    def test_prepare_sets_hooks_folder_to_the_given_directory(self, mock_path):
        mock_path.return_value.is_dir = Mock(return_value=True)
        git = Mock()

        step = ChangeHooksFolder(git)
        step.prepare(['--location', '.other'])

        mock_path.assert_called_with(getcwd(), '.other')

    def test_prepare_sets_hooks_folder_to_arguemnt_following_location(self, mock_path):
        mock_path.return_value.is_dir = Mock(return_value=True)
        git = Mock()

        step = ChangeHooksFolder(git)
        step.prepare(['some', 'args', '--location', '.other', 'and', 'some', 'more'])

        mock_path.assert_called_with(getcwd(), '.other')

    @patch('builtins.print')
    def test_prints_warning_when_nothing_follows_location(self, mock_print, mock_path):
        mock_path.return_value.is_dir = Mock(return_value=True)
        git = Mock()
        initial = git.hooks_destination

        step = ChangeHooksFolder(git)
        step.prepare(['--location'])

        mock_print.assert_called_with(('No argument following hook location flag. '
                                       'Default hooks path used instead.'))

        self.assertEqual(initial, git.hooks_destination)

    @patch('builtins.print')
    def test_prints_warning_when_given_folder_is_not_directory(self, mock_print, mock_path):
        mock_path.return_value.is_dir = Mock(return_value=False)
        git = Mock()
        initial = git.hooks_destination

        step = ChangeHooksFolder(git)
        step.prepare(['--location', 'other'])

        mock_path.return_value.is_dir = Mock(return_value=False)

        mock_print.assert_called_with((f'Not a folder: {mock_path(getcwd(), "other").absolute()}. '
                                       'Default hooks path used instead.'))
        self.assertEqual(initial, git.hooks_destination)

    def test_does_nothing_if_not_given_location_flag(self, mock_path):
        mock_path.return_value.is_dir = Mock(return_value=True)
        git = Mock()

        step = ChangeHooksFolder(git)
        step.prepare(['some', 'args', 'and', 'some', 'more'])

        git.set_hooks_destination.assert_not_called()
