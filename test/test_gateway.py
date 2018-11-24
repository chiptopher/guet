import sys
from io import StringIO
import unittest
from unittest.mock import Mock
from guet.gateway import *
from os.path import isfile, join, isdir, pardir, abspath, expanduser
import subprocess
from guet import constants as const
from guet.stdout_manager import StdoutManager
import datetime


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
        git_gateway.add_hooks()

        self.assertTrue(isfile(join(self.parent_dir, '.git', 'hooks', 'commit-msg')))

    def test_add_commit_msg_hook_adds_author_manager_scpript(self):
        git_init_process = subprocess.Popen(['git', 'init', self.parent_dir])
        git_init_process.wait()

        git_gateway = GitGateway(self.parent_dir)
        git_gateway.add_hooks()

        self.assertTrue(isfile(join(self.parent_dir, '.git', 'hooks', 'post-commit')))

    def test_commit_msg_hook_exists(self):
        git_init_process = subprocess.Popen(['git', 'init', self.parent_dir])
        git_init_process.wait()

        git_gateway = GitGateway(self.parent_dir)
        git_gateway.add_hooks()

        self.assertTrue(git_gateway.commit_msg_hook_exists())

    def test_pre_commit_hook_added_as_a_hook(self):
        git_init_process = subprocess.Popen(['git', 'init', self.parent_dir])
        git_init_process.wait()

        git_gateway = GitGateway(self.parent_dir)
        git_gateway.add_hooks()

        self.assertTrue(isfile(join(self.parent_dir, '.git', 'hooks', 'pre-commit')))


class _SQLGatewayTest(unittest.TestCase):
    def setUp(self):
        self.parent_directory = FileGateway.home_dir(__file__)
        self.settings_folder_path = join(self.parent_directory, const.APP_FOLDER_NAME)
        self.data_source_path = join(self.settings_folder_path, const.DATA_SOURCE_NAME)
        self.file_gateway = FileGateway(self.parent_directory, subprocess_module=Mock())
        self.file_gateway.initialize()
        self.connection = None

    def tearDown(self):
        if self.connection:
            self.connection.close()
        if isdir(self.settings_folder_path):
            from shutil import rmtree
            rmtree(self.settings_folder_path)


class TestPairSetCommitterGateway(_SQLGatewayTest):

    def test_add_pair_set_committer_creates_record(self):
        pair_set_committer_gateway = PairSetGatewayCommitterGateway(self.parent_directory)
        committer_initials = 'cb'
        pair_set_id = 1
        pair_set_committer_gateway.add_pair_set_committer(committer_initials, pair_set_id)

        import sqlite3

        connection = sqlite3.connect(self.data_source_path)

        cursor = connection.cursor()
        cursor.execute("SELECT * FROM pair_set_committer;")
        result = cursor.fetchall()
        self.assertEqual(1, result[0][0])
        self.assertEqual(committer_initials, result[0][1])
        self.assertEqual(pair_set_id, result[0][2])

    def test_read_pair_set_committer_by_pair_set_id(self):
        pair_set_committer_gateway = PairSetGatewayCommitterGateway(self.parent_directory)
        committer_initials = 'cb'
        pair_set_id = 1
        pair_set_committer_gateway.add_pair_set_committer(committer_initials, pair_set_id)
        result = pair_set_committer_gateway.get_pair_set_committers_by_pair_set_id(pair_set_id)
        self.assertEqual(1, len(result))
        self.assertEqual(1, result[0].id)
        self.assertEqual(pair_set_id, result[0].pair_set_id)
        self.assertEqual(committer_initials, result[0].committer_initials)


class TestPairSetGateway(_SQLGatewayTest):

    def test_add_pair_set_creates_record_with_current_time_in_millis(self):
        pair_set_gateway = PairSetGateway(self.parent_directory)
        pair_set_gateway.add_pair_set()

        result = pair_set_gateway.get_pair_set(1)
        self.assertEqual(1, result.id)
        self.assertAlmostEqual(round(datetime.datetime.utcnow().timestamp()*1000), result.set_time, -4)

    def test_add_pair_when_given_timestamp_creates_record_with_that_set_time(self):
        pair_set_gateway = PairSetGateway(self.parent_directory)
        pair_set_gateway.add_pair_set(100)

        result = pair_set_gateway.get_pair_set(1)
        self.assertEqual(1, result.id)
        self.assertEqual(100, result.set_time)

    def test_add_pair_returns_the_row_id_of_the_inserted_row(self):
        pair_set_gateway = PairSetGateway(self.parent_directory)
        rowId1 = pair_set_gateway.add_pair_set()
        self.assertEqual(1, rowId1)
        rowId2 = pair_set_gateway.add_pair_set()
        self.assertEqual(2, rowId2)

    def test_get_set_pair_by_id_returns_expected_result_set(self):
        pair_set_gateway = PairSetGateway(self.parent_directory)
        pair_set_gateway.add_pair_set(100)
        found_pair_set = pair_set_gateway.get_pair_set(1)
        self.assertEqual(100, found_pair_set.set_time)

    def test_get_most_recent_set_pair_returns_result_with_highest_set_time(self):
        pair_set_gateway = PairSetGateway(self.parent_directory)
        pair_set_gateway.add_pair_set(100)
        pair_set_gateway.add_pair_set(200)
        self.assertEqual(2, pair_set_gateway.get_most_recent_pair_set().id)


class TestUserGateway(_SQLGatewayTest):

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

    def _has_table(self, expected, result_set):
        found = False
        for result in result_set:
            if expected == result[0]:
                found = True
        return found

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

        FileGateway(parent_directory, subprocess_module=Mock()).initialize()

        self.assertTrue(isdir(self.settings_folder_path))
        self.assertTrue(isfile(data_source_path))

    def test_init_creates_data_source_properly(self):
        self.assertHasTableWithName('committer')

    def test_initialize_creates_pair_set_table(self):
        self.assertHasTableWithName('pair_set')

    def test_initialize_creates_pair_set_committer_relationship_table(self):
        self.assertHasTableWithName('pair_set_committer')

    def assertHasTableWithName(self, table_name):
        parent_directory = abspath(join(__file__, pardir))
        self.settings_folder_path = join(parent_directory, const.APP_FOLDER_NAME)
        data_source_path = join(self.settings_folder_path, const.DATA_SOURCE_NAME)
        FileGateway(parent_directory, subprocess_module=Mock()).initialize()

        import sqlite3

        connection = sqlite3.connect(data_source_path)

        cursor = connection.cursor()
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
        result = cursor.fetchall()
        self.assertTrue(self._has_table(table_name, result))

    def test_path_exists_returns_true_when_the_path_exists(self):

        parent_directory = abspath(join(__file__, pardir))
        self.settings_folder_path = join(parent_directory, const.APP_FOLDER_NAME)

        if isdir(self.settings_folder_path):
            from shutil import rmtree
            rmtree(self.settings_folder_path)

        data_source_path = join(self.settings_folder_path, const.DATA_SOURCE_NAME)

        file_gateway = FileGateway(parent_directory, subprocess_module=Mock())
        file_gateway.initialize()

        self.assertTrue(file_gateway.path_exists())

    def test_initialize_creates_committer_names_file(self):

        parent_directory = abspath(join(__file__, pardir))
        self.settings_folder_path = join(parent_directory, const.APP_FOLDER_NAME)

        if isdir(self.settings_folder_path):
            from shutil import rmtree
            rmtree(self.settings_folder_path)

        file_gateway = FileGateway(parent_directory, subprocess_module=Mock())
        file_gateway.initialize()

        committer_messages_path = join(self.settings_folder_path, const.COMMITTER_NAMES)
        self.assertTrue(isfile(committer_messages_path))

    def test_initialize_creates_author_name_and_author_email_file(self):

        parent_directory = abspath(join(__file__, pardir))
        settings_folder_path = join(parent_directory, const.APP_FOLDER_NAME)

        file_gateway = FileGateway(parent_directory, subprocess_module=Mock())
        file_gateway.initialize()

        author_names_path = abspath(join(settings_folder_path, const.AUTHOR_NAME))
        self.assertTrue(isfile(author_names_path))

    def test_set_committers_adds_the_given_committers_to_the_file(self):

        parent_directory = abspath(join(__file__, pardir))
        self.settings_folder_path = join(parent_directory, const.APP_FOLDER_NAME)
        file_gateway = FileGateway(parent_directory, subprocess_module=Mock())
        file_gateway.initialize()

        email = 'email'
        name = 'name'

        c = CommitterInput(name=name, email=email)
        file_gateway.set_committers([c])
        with open(join(parent_directory, const.APP_FOLDER_NAME, const.COMMITTER_NAMES)) as commiter_file:
            content = commiter_file.readlines()
        self.assertEqual('{} <{}>\n'.format(name, email), content[0])

    def test_set_author_name(self):
        parent_directory = abspath(join(__file__, pardir))
        self.settings_folder_path = join(parent_directory, const.APP_FOLDER_NAME)
        file_gateway = FileGateway(parent_directory, subprocess_module=Mock())
        file_gateway.initialize()

        name = 'name'
        file_gateway.set_author_name(name)
        with open(join(self.settings_folder_path, const.AUTHOR_NAME)) as author_name_file:
            content = author_name_file.readline()
        self.assertEqual(name, content)

    def test_set_author_email(self):
        parent_directory = abspath(join(__file__, pardir))
        self.settings_folder_path = join(parent_directory, const.APP_FOLDER_NAME)
        file_gateway = FileGateway(parent_directory, subprocess_module=Mock())
        file_gateway.initialize()

        email = 'email'
        file_gateway.set_author_email(email)
        with open(join(self.settings_folder_path, const.AUTHOR_EMAIL)) as author_email_file:
            content = author_email_file.readline()
        self.assertEqual(email, content)

    def test_get_committers_gets_the_list_of_current_committers(self):
        parent_directory = abspath(join(__file__, pardir))
        self.settings_folder_path = join(parent_directory, const.APP_FOLDER_NAME)
        file_gateway = FileGateway(parent_directory, subprocess_module=Mock())
        file_gateway.initialize()

        commiter1 = committer_result(initials='a', name='name name', email='email')
        commiter2 = committer_result(initials='b', name='name2', email='email2')

        expected1 = committer_result(initials='', name='name name', email='email')
        expected2 = committer_result(initials='', name='name2', email='email2')

        file_gateway.set_committers([commiter1, commiter2])
        self.assertListEqual([expected1, expected2], file_gateway.get_committers())
