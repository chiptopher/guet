from os import mkdir
from os.path import join

from guet import constants, __version__
from guet.config import CONFIGURATION_DIRECTORY
from guet.files.write_lines import write_lines


def _prepend_version_number_to_config_file():
    write_lines(join(CONFIGURATION_DIRECTORY, constants.CONFIG), [f'{__version__}\n', '\n'])


def initialize():
    mkdir(CONFIGURATION_DIRECTORY)
    _create_file_with_name(join(CONFIGURATION_DIRECTORY, constants.COMMITTER_NAMES))
    _create_file_with_name(join(CONFIGURATION_DIRECTORY, constants.AUTHOR_NAME))
    _create_file_with_name(join(CONFIGURATION_DIRECTORY, constants.AUTHOR_EMAIL))
    _create_file_with_name(join(CONFIGURATION_DIRECTORY, constants.COMMITTERS))
    _create_file_with_name(join(CONFIGURATION_DIRECTORY, constants.COMMITTERS_SET))
    _create_file_with_name(join(CONFIGURATION_DIRECTORY, constants.CONFIG))
    _create_file_with_name(join(CONFIGURATION_DIRECTORY, constants.ERRORS))
    _prepend_version_number_to_config_file()


def _create_file_with_name(file_name: str) -> None:
    open(file_name, 'w').close()
