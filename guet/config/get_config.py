from os.path import join

from guet import constants
from guet.config import configuration_directory
from guet.files.read_lines import read_lines
from guet.settings.settings import Settings


def get_config() -> Settings:
    lines = read_lines(join(configuration_directory, constants.CONFIG))
    settings = Settings()
    settings.load(lines)
    return settings
