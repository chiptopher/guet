from os.path import join

from guet import constants
from guet.config import CONFIGURATION_DIRECTORY
from guet.files.write_lines import write_lines
from guet.settings.settings import Settings


def set_config(settings: Settings) -> None:
    lines = settings.write()
    write_lines(join(CONFIGURATION_DIRECTORY, constants.CONFIG), lines)
