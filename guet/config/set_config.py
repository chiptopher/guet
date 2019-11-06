from os.path import join

from guet import constants
from guet.config import configuration_directory
from guet.files.write_lines import write_lines
from guet.settings.settings import Settings


def set_config(settings: Settings) -> None:
    lines = settings.write()
    write_lines(join(configuration_directory, constants.CONFIG), lines)
