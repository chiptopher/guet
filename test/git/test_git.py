from os.path import join
from unittest import TestCase
from unittest.mock import Mock, patch, call
from guet.git.errors import NotGuetHookError
from guet.git.git import Git

path_to_git = '/path/to/.git'


def _mock_hook(path: str):
    mock = Mock()
    mock.path = path
    return mock


@patch('guet.git.git.Hook')
class TestGit(TestCase):

    def test_init_loads_hooks_from_git_path(self, mock_hook):
        pre_commit_content = Mock()
        post_commit_content = Mock()
        commit_msg_content = Mock()
        expected_hooks = [pre_commit_content, post_commit_content, commit_msg_content]
        mock_hook.side_effect = expected_hooks

        git = Git(path_to_git)

        mock_hook.assert_has_calls([
            call(join(path_to_git, 'hooks', 'pre-commit')),
            call(join(path_to_git, 'hooks', 'post-commit')),
            call(join(path_to_git, 'hooks', 'commit-msg'))
        ])
        self.assertListEqual(expected_hooks, git.hooks)

    def test_init_trys_dash_guet_for_file_name_if_name_without_dash_fails(self, mock_hook):
        pre_commit_content = Mock()
        post_commit_content = Mock()
        commit_msg_content = Mock()
        expected_hooks = [pre_commit_content, post_commit_content, commit_msg_content]
        mock_hook.side_effect = [pre_commit_content, post_commit_content, NotGuetHookError(), commit_msg_content]

        git = Git(path_to_git)

        mock_hook.assert_has_calls([
            call(join(path_to_git, 'hooks', 'pre-commit')),
            call(join(path_to_git, 'hooks', 'post-commit')),
            call(join(path_to_git, 'hooks', 'commit-msg')),
            call(join(path_to_git, 'hooks', 'commit-msg-guet'))
        ])
        self.assertListEqual(expected_hooks, git.hooks)

    def test_init_swallows_file_not_found_error(self, mock_hook):
        mock_hook.side_effect = [FileNotFoundError(), FileNotFoundError(), FileNotFoundError(), FileNotFoundError(),
                                 FileNotFoundError(), FileNotFoundError()]

        git = Git(path_to_git)

        self.assertListEqual([], git.hooks)

    def test_hooks_present_returns_true_when_all_normal_hooks_present(self, mock_hook):
        git = Git(path_to_git)
        git.hooks = [
            _mock_hook(join(path_to_git, 'hooks', 'pre-commit')),
            _mock_hook(join(path_to_git, 'hooks', 'post-commit')),
            _mock_hook(join(path_to_git, 'hooks', 'commit-msg'))
        ]
        self.assertTrue(git.hooks_present())

    def test_hooks_present_when_all_dash_guet_hooks_are_present(self, mock_hook):
        git = Git(path_to_git)
        git.hooks = [
            _mock_hook(join(path_to_git, 'hooks', 'pre-commit-guet')),
            _mock_hook(join(path_to_git, 'hooks', 'post-commit-guet')),
            _mock_hook(join(path_to_git, 'hooks', 'commit-msg-guet'))
        ]
        self.assertTrue(git.hooks_present())
