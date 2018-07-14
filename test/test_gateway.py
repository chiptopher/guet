import sys
from io import StringIO
import unittest
from guet.gateway import *
from os.path import isfile, join, isdir, pardir, abspath, expanduser
import subprocess
from guet import constants as const
from guet.stdout_manager import StdoutManager


class TestPrintGateway(unittest.TestCase):

    def setUp(self):
        self.original_stdout = sys.stdout

    def tearDown(self):
        sys.stdout = self.original_stdout

    def test_init_set_the_stdout_as_the_default_system_stdout(self):
        print_gateway = PrintGateway()
        self.assertEqual(StdoutManager.get_instance(), print_gateway._stdout_manager)

    def test_print_writes_to_stdout(self):
        stdout = StringIO()
        stdout_manager = StdoutManager.get_instance()
        stdout_manager.set_stdout(stdout)
        print_gateway = PrintGateway(stdout_manager)
        text = 'text'
        print_gateway.print(text)
        self.assertEqual(text + '\n', stdout.getvalue())


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
        git_gateway.add_commit_msg_hook()

        self.assertTrue(isfile(join(self.parent_dir, '.git', 'hooks', 'commit-msg')))

    def test_commit_msg_hook_exists(self):
        git_init_process = subprocess.Popen(['git', 'init', self.parent_dir])
        git_init_process.wait()

        git_gateway = GitGateway(self.parent_dir)
        git_gateway.add_commit_msg_hook()

        self.assertTrue(git_gateway.commit_msg_hook_exists())


class TestUserGateway(unittest.TestCase):

    def setUp(self):
        self.parent_directory = FileGateway.home_dir(__file__)
        self.settings_folder_path = join(self.parent_directory, const.APP_FOLDER_NAME)
        self.data_source_path = join(self.settings_folder_path, const.DATA_SOURCE_NAME)
        self.file_gateway = FileGateway(self.parent_directory)
        self.file_gateway.initialize()
        self.connection = None

    def tearDown(self):
        if self.connection:
            self.connection.close()
        if isdir(self.settings_folder_path):
            from shutil import rmtree
            rmtree(self.settings_folder_path)

    def test_default_connection_path_is_data_source_in_user_home_directory(self):
        user_gateway = UserGateway()
        expected_path = join(expanduser('~'), join(const.APP_FOLDER_NAME, const.DATA_SOURCE_NAME))
        self.assertEqual(expected_path, user_gateway._connection_path)

    def test_add_user_can_add_user(self):

        user_gateway = UserGateway(self.parent_directory)
        initials = 'up'
        name = 'userperson'
        email = 'userperson@localhost'
        user_gateway.add_user(initials, name, email)
        result = user_gateway.get_user(initials)
        self.assertEqual(initials, result.initials)
        self.assertEqual(name, result.name)
        self.assertEqual(email, result.email)

    def test_remove_user(self):

        user_gateway = UserGateway(self.parent_directory)
        initials = 'up'
        user_gateway.add_user(initials, 'name', 'email')
        user_gateway.delete_user(initials)
        self.assertIsNone(user_gateway.get_user(initials))

    def test_add_user_with_duplicate_initials_should_overwrite_existing_one(self):
        user_gateway = UserGateway(self.parent_directory)
        initials = 'up'
        name = 'userperson'
        email = 'userperson@localhost'
        user_gateway.add_user(initials, name, email)
        new_name = 'newname'
        user_gateway.add_user(initials, new_name, email)
        result = user_gateway.get_user(initials)
        self.assertEqual(new_name, result[1])


class TestFileGateway(unittest.TestCase):

    settings_folder_path = None

    def setUp(self):
        self.settings_folder_path = None

    def tearDown(self):

        if self.settings_folder_path:
            from shutil import rmtree
            rmtree(self.settings_folder_path)

    def test_init_sets_default_path_to_home_directory(self):

        file_gateway = FileGateway()
        from os.path import expanduser
        self.assertEqual(expanduser("~"), file_gateway._path)

    def test_init_creates_folder_at_with_data_source_at_given_path(self):

        from os.path import pardir, join, abspath, isfile, isdir

        parent_directory = abspath(join(__file__, pardir))
        self.settings_folder_path = join(parent_directory, const.APP_FOLDER_NAME)
        data_source_path = join(self.settings_folder_path, const.DATA_SOURCE_NAME)

        FileGateway(parent_directory).initialize()

        self.assertTrue(isdir(self.settings_folder_path))
        self.assertTrue(isfile(data_source_path))

    def test_init_creates_data_source_properly(self):

        parent_directory = abspath(join(__file__, pardir))
        self.settings_folder_path = join(parent_directory, const.APP_FOLDER_NAME)
        data_source_path = join(self.settings_folder_path, const.DATA_SOURCE_NAME)

        FileGateway(parent_directory).initialize()

        import sqlite3

        connection = sqlite3.connect(data_source_path)

        cursor = connection.cursor()
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
        result = cursor.fetchall()
        self.assertEqual(1, len(result))
        self.assertEqual('committer', result[0][0])
        connection.close()

    def test_path_exists_returns_true_when_the_path_exists(self):

        parent_directory = abspath(join(__file__, pardir))
        self.settings_folder_path = join(parent_directory, const.APP_FOLDER_NAME)

        if isdir(self.settings_folder_path):
            from shutil import rmtree
            rmtree(self.settings_folder_path)

        data_source_path = join(self.settings_folder_path, const.DATA_SOURCE_NAME)

        file_gateway = FileGateway(parent_directory)
        file_gateway.initialize()

        self.assertTrue(file_gateway.path_exists())

    def test_initialize_creates_committer_names_file(self):

        parent_directory = abspath(join(__file__, pardir))
        settings_folder_path = join(parent_directory, const.APP_FOLDER_NAME)

        file_gateway = FileGateway(parent_directory)
        file_gateway.initialize()

        committer_messages_path = join(settings_folder_path, const.COMMITTER_NAMES)
        self.assertTrue(isfile(committer_messages_path))

    def test_set_committers_adds_the_given_committers_to_the_file(self):

        parent_directory = abspath(join(__file__, pardir))
        self.settings_folder_path = join(parent_directory, const.APP_FOLDER_NAME)
        file_gateway = FileGateway(parent_directory)
        file_gateway.initialize()

        email = 'email'
        name = 'name'

        c = CommitterInput(name=name, email=email)
        file_gateway.set_committers([c])
        with open(join(parent_directory, const.APP_FOLDER_NAME, const.COMMITTER_NAMES)) as commiter_file:
            content = commiter_file.readlines()
        self.assertEqual('{} <{}>\n'.format(name, email), content[0])
