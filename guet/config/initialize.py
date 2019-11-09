from os import mkdir
from os.path import join

from guet import constants, __version__
from guet.config import configuration_directory
from guet.files.write_lines import write_lines


def _prepend_version_number_to_config_file():
    write_lines(join(configuration_directory, constants.CONFIG), [f'{__version__}\n', '\n'])


def initialize():
    mkdir(configuration_directory)
    _create_file_with_name(join(configuration_directory, constants.COMMITTER_NAMES))
    _create_file_with_name(join(configuration_directory, constants.AUTHOR_NAME))
    _create_file_with_name(join(configuration_directory, constants.AUTHOR_EMAIL))
    _create_file_with_name(join(configuration_directory, constants.COMMITTERS))
    _create_file_with_name(join(configuration_directory, constants.COMMITTERS_SET))
    _create_file_with_name(join(configuration_directory, constants.CONFIG))
    _prepend_version_number_to_config_file()


def _create_file_with_name(file_name: str) -> None:
    open(file_name, 'w').close()
