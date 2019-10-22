import unittest
from unittest.mock import Mock

from os.path import abspath, join

from guet import constants as const
from guet.gateways.gateway import *


class _SQLGatewayTest(unittest.TestCase):
    def setUp(self):
        self.parent_directory = abspath(join(__file__, pardir))
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
