import subprocess
import unittest
from os.path import join, isfile, isdir

from guet.gateways.gateway import FileGateway
from guet.git.git_gateway import GitGateway


class TestGitGateway(unittest.TestCase):

    def setUp(self):
        self.parent_dir = FileGateway.home_dir(__file__)

    def tearDown(self):
        git_path = join(self.parent_dir, '.git')
        if isdir(git_path):
            from shutil import rmtree
            rmtree(git_path)

    def test_add_commit_msg_hook(self):
        git_init_process = subprocess.Popen(['git', 'init', self.parent_dir])
        git_init_process.wait()

        git_gateway = GitGateway(self.parent_dir)
        git_gateway.add_hooks(GitGateway.DEFAULT)

        self.assertTrue(isfile(join(self.parent_dir, '.git', 'hooks', 'commit-msg')))

    def test_add_commit_msg_hook_adds_author_manager_scpript(self):
        git_init_process = subprocess.Popen(['git', 'init', self.parent_dir])
        git_init_process.wait()

        git_gateway = GitGateway(self.parent_dir)
        git_gateway.add_hooks(GitGateway.DEFAULT)

        self.assertTrue(isfile(join(self.parent_dir, '.git', 'hooks', 'post-commit')))

    def test_commit_msg_hook_exists(self):
        git_init_process = subprocess.Popen(['git', 'init', self.parent_dir])
        git_init_process.wait()

        git_gateway = GitGateway(self.parent_dir)
        git_gateway.add_hooks(GitGateway.DEFAULT)

        self.assertTrue(git_gateway.commit_msg_hook_exists())

    def test_pre_commit_hook_added_as_a_hook(self):
        git_init_process = subprocess.Popen(['git', 'init', self.parent_dir])
        git_init_process.wait()

        git_gateway = GitGateway(self.parent_dir)
        git_gateway.add_hooks(GitGateway.DEFAULT)

        self.assertTrue(isfile(join(self.parent_dir, '.git', 'hooks', 'pre-commit')))

    def test_hook_exists_can_tell_if_given_hook_exists(self):
        git_init_process = subprocess.Popen(['git', 'init', self.parent_dir])
        git_init_process.wait()

        git_gateway = GitGateway(self.parent_dir)
        git_gateway.add_hooks(GitGateway.DEFAULT)

        self.assertTrue(git_gateway.hook_present('pre-commit'))
        self.assertFalse(git_gateway.hook_present('not-a-hook'))

    def test_add_hooks_creates_hook_files_with_guet_prependend_to_name_when_given_create_alongside_flag(self):
        git_init_process = subprocess.Popen(['git', 'init', self.parent_dir])
        git_init_process.wait()

        git_gateway = GitGateway(self.parent_dir)
        git_gateway.add_hooks(GitGateway.CREATE_ALONGSIDE)
        self.assertTrue(git_gateway.hook_present('guet-pre-commit'))

    def test_add_hooks_doesnt_create_hook_files_when_given_cancel_flag(self):
        git_init_process = subprocess.Popen(['git', 'init', self.parent_dir])
        git_init_process.wait()

        git_gateway = GitGateway(self.parent_dir)
        git_gateway.add_hooks(GitGateway.CANCEL)
        self.assertFalse(git_gateway.hook_present('pre-commit'))

    def test_add_hooks_overwrites_previous_hook_when_given_overwrite_flag(self):
        git_init_process = subprocess.Popen(['git', 'init', self.parent_dir])
        git_init_process.wait()

        f = open(join(self.parent_dir, '.git', 'hooks', 'pre-commit'), 'w+')
        f.write('Text')
        f.close()

        git_gateway = GitGateway(self.parent_dir)
        git_gateway.add_hooks(GitGateway.OVERWRITE)

        f = open(join(self.parent_dir, '.git', 'hooks', 'pre-commit'), 'r')
        data = f.readlines()
        f.close()
        self.assertNotEqual(1, len(data), 'Should have more than one line because pre-commit file is being overwritten')

    def test_add_hooks_with_init_python3_flag_as_true_sets_the_interpreter_to_python3_for_pre_and_post_commit(self):
        git_init_process = subprocess.Popen(['git', 'init', self.parent_dir])
        git_init_process.wait()

        git_gateway = GitGateway(self.parent_dir)
        git_gateway.add_hooks(GitGateway.DEFAULT, True)

        file_name = join(self.parent_dir, '.git', 'hooks', 'post-commit')
        with open(file_name) as f:
            first_line = f.readline().rstrip()
        self.assertTrue(first_line.endswith('python3'), '{} should end with python3'.format(first_line))

        file_name = join(self.parent_dir, '.git', 'hooks', 'pre-commit')
        with open(file_name) as f:
            first_line = f.readline().rstrip()
        self.assertTrue(first_line.endswith('python3'), '{} should end with python3'.format(first_line))

