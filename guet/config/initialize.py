from os import mkdir
from os.path import expanduser, join
import sqlite3

from guet import constants
from guet.config import configuration_directory


def initialize():
    mkdir(configuration_directory)
    _create_file_with_name(join(configuration_directory, constants.COMMITTER_NAMES))
    _create_file_with_name(join(configuration_directory, constants.AUTHOR_NAME))
    _create_file_with_name(join(configuration_directory, constants.AUTHOR_EMAIL))
    _create_file_with_name(join(configuration_directory, constants.COMMITTERS))
    _create_file_with_name(join(configuration_directory, constants.COMMITTERS_SET))
    _create_file_with_name(join(configuration_directory, constants.CONFIG))


def _create_file_with_name(file_name: str) -> None:
    open(file_name, 'w').close()

