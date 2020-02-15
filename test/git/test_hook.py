from unittest import TestCase
from unittest.mock import patch

from guet.git.errors import NotGuetHookError
from guet.git.hook import Hook, GUET_HOOK_FILE


@patch('guet.git.hook.read_lines', return_value=GUET_HOOK_FILE)
class TestHook(TestCase):

    def test_reads_content_to_hook(self, mock_read_lines):
        hook = Hook('/path/to/.git/hooks/name')
        mock_read_lines.assert_called_with('/path/to/.git/hooks/name')
        self.assertEqual(mock_read_lines.return_value, hook.content)

    def test_throws_error_when_path_is_to_non_guet_hook(self, mock_read_lines):
        mock_read_lines.return_value = ['Other', 'Content']
        try:
            hook = Hook('/path/to/.git/hooks/name')
            self.fail('Should raise Exception')
        except NotGuetHookError:
            pass

    def test_works_with_specific_content(self, mock_read_lines):
        mock_read_lines.return_value = ['#! /usr/bin/env python3', 'from guet.hooks import manage', 'import sys',
                                        'manage(sys.argv[0])']
        try:
            hook = Hook('/path/to/.git/hooks/name')
            pass
        except (NotGuetHookError, FileNotFoundError):
            self.fail('Should successfully create hook.')
