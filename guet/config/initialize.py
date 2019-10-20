from os import mkdir
from os.path import expanduser, join
import sqlite3

from guet import constants
from guet.config import configuration_directory


def initialize():
    mkdir(configuration_directory)
    connection = sqlite3.connect(join(configuration_directory, constants.DATA_SOURCE_NAME))
    _create_committer_table(connection)
    _create_pair_set_table(connection)
    _create_pair_set_committer_join_table(connection)
    connection.close()
    _create_file_with_name(join(configuration_directory, constants.COMMITTER_NAMES))
    _create_file_with_name(join(configuration_directory, constants.AUTHOR_NAME))
    _create_file_with_name(join(configuration_directory, constants.AUTHOR_EMAIL))


def _create_file_with_name(file_name: str) -> None:
    open(file_name, 'w').close()


def _create_pair_set_committer_join_table(connection):
    connection.execute("""CREATE TABLE pair_set_committer
                              (id INTEGER NOT NULL PRIMARY KEY,
                              committer_initials TEXT NOT NULL,
                              pair_set_id INTEGER NOT NULL,
                              FOREIGN KEY (pair_set_id) REFERENCES pair_set(id),
                              FOREIGN KEY (committer_initials) REFERENCES comitter(initials)
                              )
                              """)


def _create_pair_set_table(connection):
    connection.execute("""CREATE TABLE pair_set
                              (id INTEGER NOT NULL PRIMARY KEY,
                              set_time INTEGER NOT NULL)
                              """)


def _create_committer_table(connection) -> None:
    connection.execute("""CREATE TABLE committer
                              (initials TEXT NOT NULL PRIMARY KEY,
                               name TEXT NOT NULL,
                               email TEXT NOT NULL)""")
