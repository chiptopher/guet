from os.path import join
from pathlib import Path

from guet import constants
from guet.config import CONFIGURATION_DIRECTORY
from guet.files.read_lines import read_lines
from guet.settings.settings import Settings


def get_settings() -> Settings:
    lines = read_lines(Path(join(CONFIGURATION_DIRECTORY, constants.CONFIG)))
    settings = Settings()
    settings.load(lines)
    return settings
