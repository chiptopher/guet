from pathlib import Path
from unittest import TestCase
from unittest.mock import Mock, patch

from guet.git.errors import NotGuetHookError
from guet.git.hook import PYTHON3_GUET_HOOK, PYTHON_GUET_HOOK, Hook


@patch('guet.git.hook.which', return_value='/path/to/python3')
@patch('guet.git.hook.read_lines', return_value=PYTHON3_GUET_HOOK)
class TestHook(TestCase):

    def test_reads_content_to_hook(self, mock_read_lines, mock_which):
        path = Path('/path/to/.git/hooks/name')
        hook = Hook(path)
        mock_read_lines.assert_called_with(path)
        self.assertEqual(mock_read_lines.return_value, hook.content)

    def test_is_guet_hook_returns_whether_hook_matches_guet_content(self, mock_read_lines, mock_which):
        mock_read_lines.return_value = ['Other', 'Content']
        hook = Hook(Path('/path/to/.git/hooks/name'))
        self.assertFalse(hook.is_guet_hook())

    def test_works_with_specific_content(self, mock_read_lines, mock_which):
        mock_read_lines.return_value = ['#! /usr/bin/env python3', 'from guet.hooks import manage', 'import sys',
                                        'manage(sys.argv[0])']
        try:
            Hook(Path('/path/to/.git/hooks/name'))
            pass
        except (NotGuetHookError, FileNotFoundError):
            self.fail('Should successfully create hook.')

    def test_init_with_create_flag_catches_file_not_found_error_and_save_content_to_default(self, mock_read_lines,
                                                                                            mock_which):
        mock_read_lines.side_effect = FileNotFoundError()
        hook = Hook(Path('/path/to/.git/hooks/name'), create=True)
        self.assertEqual(PYTHON3_GUET_HOOK, hook.content)

    def test_init_with_create_flag_overwrites_already_present_content(self, mock_read_lines, mock_which):
        mock_read_lines.return_value = ['Other', 'Content']
        hook = Hook(Path('/path/to/.git/hooks/name'), create=True)
        self.assertEqual(PYTHON3_GUET_HOOK, hook.content)

    @patch('guet.git.hook.chmod')
    @patch('guet.git.hook.stat')
    @patch('guet.git.hook.write_lines')
    def test_save_writes_lines_to_file(self, mock_write_lines, mock_stat, mock_chmod, mock_read_lines, mock_which):
        mock_read_lines.side_effect = FileNotFoundError()
        mock_path = Mock()
        hook = Hook(mock_path, create=True)
        hook.save()
        mock_write_lines.assert_called_with(mock_path, hook.content)

    @patch('guet.git.hook.chmod')
    @patch('guet.git.hook.stat')
    @patch('guet.git.hook.write_lines')
    def test_save_chmods_file_to_executable(self, mock_write_lines, mock_stat, mock_chmod, mock_read_lines, mock_which):
        mock_read_lines.side_effect = FileNotFoundError()
        path = '/path/to/.git/hooks/name'
        mock_path = Mock()
        mock_path.__str__ = Mock(return_value=path)
        hook = Hook(mock_path, create=True)
        hook.save()
        mock_chmod.assert_called_with(path, mock_stat.return_value.st_mode | 0o111)

    def test_is_get_hook_registers_python_shebang_without_the_3_as_guet_hook(self, mock_read_lines, mock_which):
        mock_read_lines.return_value = PYTHON_GUET_HOOK
        path = '/path/to/.git/hooks/name'
        hook = Hook(Path(path))
        self.assertTrue(hook.is_guet_hook())

    @patch('guet.git.hook.chmod')
    @patch('guet.git.hook.stat')
    @patch('guet.git.hook.write_lines')
    def test_uses_python_if_python3_is_not_available(self, mock_write_lines, mock_stat, mock_chmod, mock_read_lines,
                                                     mock_which):
        mock_which.return_value = None
        mock_read_lines.side_effect = FileNotFoundError()
        path = Mock()
        hook = Hook(path, create=True)
        hook.save()
        mock_write_lines.assert_called_with(path, PYTHON_GUET_HOOK)
