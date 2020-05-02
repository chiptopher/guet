from os.path import join
from pathlib import Path
from unittest import TestCase
from unittest.mock import Mock, patch, call

from guet.committers.committer import Committer
from guet.git.author import Author
from guet.git.errors import NoGitPresentError
from guet.git.git import Git

default_config_response = ['[core]',
                           '\trepositoryformatversion = 0',
                           '\tfilemode = true',
                           '\tbare = false',
                           '\tlogallrefupdates = true',
                           '\tignorecase = true',
                           '\tprecomposeunicode = true',
                           '[user]',
                           '\tname = name',
                           '\temail = name@localhost'
                           ]


def _mock_hook(path: str, *, is_guet_hook: bool = True):
    mock = Mock()
    mock.path = path
    mock.is_guet_hook.return_value = is_guet_hook
    return mock


def _mock_repository_path(*, is_dir=True) -> Path:
    mock = Mock()
    mock.is_dir.return_value = is_dir
    return mock


_mock_read_lines = [['First line of commit message', 'Second line of commit message'], default_config_response]


@patch('guet.git.git.read_lines', side_effect=_mock_read_lines)
@patch('guet.git._hook_loader.Hook')
class TestGit(TestCase):
    def setUp(self) -> None:
        self.path_to_git = _mock_repository_path()

    def test_init_loads_all_possible_hooks(self, mock_hook, _1):
        pre_commit_content = Mock()
        post_commit_content = Mock()
        commit_msg_content = Mock()
        pre_commit_alongside_content = Mock()
        post_commit_alongside_content = Mock()
        commit_msg_alongside_content = Mock()

        expected_hooks = [pre_commit_content, post_commit_content, commit_msg_content,
                          pre_commit_alongside_content, post_commit_alongside_content, commit_msg_alongside_content]

        mock_hook.side_effect = expected_hooks

        git = Git(self.path_to_git)

        mock_hook.assert_has_calls([
            call(self.path_to_git.joinpath('hooks').joinpath('pre-commit'), create=False),
            call(self.path_to_git.joinpath('hooks').joinpath('post-commit'), create=False),
            call(self.path_to_git.joinpath('hooks').joinpath('commit-msg'), create=False),
            call(self.path_to_git.joinpath('hooks').joinpath('pre-commit-guet'), create=False),
            call(self.path_to_git.joinpath('hooks').joinpath('post-commit-guet'), create=False),
            call(self.path_to_git.joinpath('hooks').joinpath('commit-msg-guet'), create=False),
        ])
        self.assertListEqual(expected_hooks, git.hooks)

    def test_init_swallows_file_not_found_error(self, mock_hook, _1):
        mock_hook.side_effect = [FileNotFoundError(), FileNotFoundError(), FileNotFoundError(), FileNotFoundError(),
                                 FileNotFoundError(), FileNotFoundError()]

        git = Git(self.path_to_git)

        self.assertListEqual([], git.hooks)

    def test_init_loads_current_commit_msg(self, _1, mock_read_lines):
        expected_commit_msg = ['First line of commit message', 'Second line of commit message']
        mock_read_lines.return_value = expected_commit_msg
        git = Git(self.path_to_git)
        self.assertListEqual(expected_commit_msg, git.commit_msg)

    def test_init_handles_there_not_being_a_commit_msg_file_becuase_of_no_commits(self, _1, mock_read_lines):
        mock_read_lines.side_effect = [
            FileNotFoundError(),
            default_config_response
        ]
        git = Git(self.path_to_git)
        self.assertListEqual([], git.commit_msg)

    def test_init_throws_no_git_present_error_when_git_isnt_there(self, _1, _2):
        missing_directory = _mock_repository_path(is_dir=False)
        try:
            Git(missing_directory)
            self.fail('Should raise exception')
        except NoGitPresentError:
            pass

    def test_init_loads_the_author_from_the_config_file(self, _1, _2):
        git = Git(self.path_to_git)
        self.assertEqual('name', git.author.name)
        self.assertEqual('name@localhost', git.author.email)

    def test_init_loads_none_when_there_is_no_author_set_in_config(self, _1, mock_read_lines):
        without_author = list(default_config_response)
        del without_author[-1]
        del without_author[-2]
        del without_author[-3]
        mock_read_lines.side_effect = [
            [],
            without_author
        ]
        git = Git(self.path_to_git)
        self.assertIsNone(git.author)

    @patch('guet.git.git.write_lines')
    def test_setting_commit_msg_writes_it_to_file(self, mock_write_lines, _1, _2):
        new_content = ['New line 1', 'New line 2']
        git = Git(self.path_to_git)
        git.commit_msg = new_content
        mock_write_lines.assert_called_with(self.path_to_git.joinpath('COMMIT_EDITMSG'), new_content)

    @patch('guet.git.git.write_lines')
    def test_setting_author_writes_it_to_file(self, mock_write_lines, _1, _2):
        new_content = list(default_config_response)
        new_content[-1] = '\temail = new_email@localhost'
        new_content[-2] = '\tname = new_name'

        git = Git(self.path_to_git)
        git.author = Author(name='new_name', email='new_email@localhost')
        mock_write_lines.assert_called_with(self.path_to_git.joinpath('config'), new_content)


@patch('guet.git.git.write_lines')
def test_setting_writes_author_when_no_author_currently_present(self, mock_write_lines, _1):
    content_without_author = list(default_config_response)
    del content_without_author[-1]
    del content_without_author[-1]
    del content_without_author[-1]

    new_content = content_without_author + ['[user]', '\tname = new_name', '\temail = new_email@localhost']

    git = Git(self.path_to_git)
    git._config_lines = content_without_author
    git.author = Author(name='new_name', email='new_email@localhost')
    mock_write_lines.assert_called_with(self.path_to_git.joinpath('config'), new_content)


def test_hooks_present_returns_true_when_all_normal_hooks_present(self, _1, _2):
    git = Git(self.path_to_git)
    git.hooks = [
        _mock_hook(join(str(self.path_to_git), 'hooks', 'pre-commit')),
        _mock_hook(join(str(self.path_to_git), 'hooks', 'post-commit')),
        _mock_hook(join(str(self.path_to_git), 'hooks', 'commit-msg'))
    ]
    self.assertTrue(git.hooks_present())


def test_hooks_present_returns_false_if_normal_hooks_have_non_guet_content(self, _1, _2):
    git = Git(self.path_to_git)
    git.hooks = [
        _mock_hook(join(str(self.path_to_git), 'hooks', 'pre-commit')),
        _mock_hook(join(str(self.path_to_git), 'hooks', 'post-commit'), is_guet_hook=False),
        _mock_hook(join(str(self.path_to_git), 'hooks', 'commit-msg'))
    ]
    self.assertFalse(git.hooks_present())


def test_hooks_present_returns_true_when_normal_hooks_have_non_guet_content_but_dash_hooks_are_present(self, _1,
                                                                                                       _2):
    git = Git(self.path_to_git)
    git.hooks = [
        _mock_hook(join(str(self.path_to_git), 'hooks', 'post-commit'), is_guet_hook=False),
        _mock_hook(join(str(self.path_to_git), 'hooks', 'pre-commit-guet')),
        _mock_hook(join(str(self.path_to_git), 'hooks', 'post-commit-guet')),
        _mock_hook(join(str(self.path_to_git), 'hooks', 'commit-msg-guet'))
    ]
    self.assertTrue(git.hooks_present())


def test_hooks_present_when_all_dash_guet_hooks_are_present(self, _1, _2):
    git = Git(self.path_to_git)
    git.hooks = [
        _mock_hook(join(str(self.path_to_git), 'hooks', 'pre-commit-guet')),
        _mock_hook(join(str(self.path_to_git), 'hooks', 'post-commit-guet')),
        _mock_hook(join(str(self.path_to_git), 'hooks', 'commit-msg-guet'))
    ]
    self.assertTrue(git.hooks_present())


def test_non_guet_hooks_present_returns_true_if_any_hooks_have_non_guet_contnet(self, _1, _2):
    git = Git(self.path_to_git)
    non_guet_hook = Mock()
    non_guet_hook.is_guet_hook.return_value = False
    guet_hook = Mock()
    guet_hook.is_guet_hook.return_value = True
    git.hooks = [non_guet_hook]
    self.assertTrue(git.non_guet_hooks_present())


def test_non_guet_hooks_present_returns_false_if_all_hooks_have_guet_content(self, _1, _2):
    git = Git(self.path_to_git)
    guet_hook = Mock()
    guet_hook.is_guet_hook.return_value = True
    git.hooks = [guet_hook]
    self.assertFalse(git.non_guet_hooks_present())


def test_non_guet_hook_present_returns_false_when_no_hooks_present(self, _1, _2):
    git = Git(self.path_to_git)
    git.hooks = []
    self.assertFalse(git.non_guet_hooks_present())


def test_create_hooks_adds_new_files(self, mock_hook, _2):
    git = Git(self.path_to_git)
    git.hooks = []

    mock_hook.reset_mock()
    pre_commit_hook = Mock()
    post_commit_hook = Mock()
    commit_msg_hook = Mock()
    expected_hooks = [pre_commit_hook, post_commit_hook, commit_msg_hook]
    mock_hook.side_effect = expected_hooks

    git.create_hooks()

    self.assertListEqual(expected_hooks, git.hooks)

    mock_hook.assert_has_calls([
        call(self.path_to_git.joinpath('hooks').joinpath('pre-commit'), create=True),
        call(self.path_to_git.joinpath('hooks').joinpath('post-commit'), create=True),
        call(self.path_to_git.joinpath('hooks').joinpath('commit-msg'), create=True),
    ])

    pre_commit_hook.save.assert_called()
    post_commit_hook.save.assert_called()
    commit_msg_hook.save.assert_called()


def test_create_hooks_adds_new_alongside_hooks(self, mock_hook, _1, _2):
    git = Git(self.path_to_git)
    git.hooks = []

    mock_hook.reset_mock()
    pre_commit_hook = Mock()
    post_commit_hook = Mock()
    commit_msg_hook = Mock()
    expected_hooks = [pre_commit_hook, post_commit_hook, commit_msg_hook]
    mock_hook.side_effect = expected_hooks

    git.create_hooks(alongside=True)

    self.assertListEqual(expected_hooks, git.hooks)

    mock_hook.assert_has_calls([
        call(self.path_to_git.joinpath('hooks').joinpath('pre-commit-guet'), create=True),
        call(self.path_to_git.joinpath('hooks').joinpath('post-commit-guet'), create=True),
        call(self.path_to_git.joinpath('hooks').joinpath('commit-msg-guet'), create=True),
    ])

    pre_commit_hook.save.assert_called()
    post_commit_hook.save.assert_called()
    commit_msg_hook.save.assert_called()


@patch('guet.git.git.write_lines')
def test_notify_of_author_sets_the_author_proprty(self, mock_write_lines, _1, _2):
    git = Git(self.path_to_git)
    committer = Committer(name='new_name', email='new_email', initials='initials')
    git.notify_of_committer_set([committer])
    self.assertEqual('new_name', git.author.name)
    self.assertEqual('new_email', git.author.email)
