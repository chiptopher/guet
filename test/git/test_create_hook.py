import unittest
from unittest.mock import patch

from guet.git.create_hook import Hooks, create_hook, HookMode


MOCK_ST_MODE = 1


class MockStat:
    def __init__(self):
        self.st_mode = MOCK_ST_MODE


# os.chmod(hook_path, st.st_mode | 0o111)
@patch('guet.git.create_hook.stat')
@patch('guet.git.create_hook.chmod')
class TestCreateHook(unittest.TestCase):

    @patch('builtins.open', new_callable=unittest.mock.mock_open())
    def test_create_hook_with_hook_mode_create_alongside_appends_guet_to_file_name(self, mock_open, mock_chmod, mock_state):
        create_hook('path', Hooks.PRE_COMMIT, HookMode.CREATE_ALONGSIDE)
        mock_open.assert_called_once_with('path/pre-commit-guet', 'w')

    @patch('builtins.open', new_callable=unittest.mock.mock_open())
    def test_create_hooks_makes_hook_executable(self, mock_open, mock_chmod, mock_stat):
        mock_stat.return_value = MockStat()
        create_hook('path', Hooks.PRE_COMMIT, HookMode.NEW_OR_OVERWRITE)
        mock_chmod.assert_called_with('path/pre-commit', MOCK_ST_MODE | 0o111)


    @patch('builtins.open', new_callable=unittest.mock.mock_open())
    def test_create_hook_pre_commit_writes_precommit_text_to_file(self, mock_open, mock_chmod, mock_stat):
        create_hook('path', Hooks.PRE_COMMIT, HookMode.NEW_OR_OVERWRITE)
        mock_open.assert_called_once_with('path/pre-commit', 'w')
        mock_open.return_value.writelines.assert_called_with([
            '#! /usr/bin/env python3\n',
            'from guet.commit import PreCommitManager\n',
            'cm = PreCommitManager()\n',
            'cm.manage()\n'
        ])

        mock_open.return_value.close.assert_called()


    @patch('builtins.open', new_callable=unittest.mock.mock_open())
    def test_create_hook_sets_hook_file_to_executable(self, mock_open, mock_chmod, mock_stat):
        create_hook('path', Hooks.POST_COMMIT, HookMode.NEW_OR_OVERWRITE)


    @patch('builtins.open', new_callable=unittest.mock.mock_open())
    def test_create_hook_commit_msg_writes_commitmsg_text_to_file(self, mock_open, mock_chmod, mock_stat):
        create_hook('path', Hooks.COMMIT_MSG, HookMode.NEW_OR_OVERWRITE)
        mock_open.assert_called_once_with('path/commit-msg', 'w')
        mock_open.return_value.writelines.assert_called_with([
            "#!/bin/sh\n",
            "FILE_LOCATION=~/.guet/committernames\n",
            'CO_AUTHOR="Co-authored-by:"\n',
            'echo "\\n\\n" >> "$1"\n',
            'while read committer; do\n',
            '	echo "$CO_AUTHOR $committer" >> "$1"\n',
            'done <$FILE_LOCATION\n'
        ])
        mock_open.return_value.close.assert_called()

    @patch('builtins.open', new_callable=unittest.mock.mock_open())
    def test_create_hook_post_commit_writes_postcommit_text_to_file(self, mock_open, mock_chmod, mock_stat):
        create_hook('path', Hooks.POST_COMMIT, HookMode.NEW_OR_OVERWRITE)
        mock_open.assert_called_once_with('path/post-commit', 'w')
        mock_open.return_value.writelines.assert_called_with([
            '#! /usr/bin/env python3\n',
            'from guet.commit import PostCommitManager\n',
            'cm = PostCommitManager()\n',
            'cm.manage()\n'
        ])

        mock_open.return_value.close.assert_called()
