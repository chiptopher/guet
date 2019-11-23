from os.path import join
from typing import List

from guet import constants
from guet.config import CONFIGURATION_DIRECTORY
from guet.files.write_lines import write_lines


def set_errors(error_lines: List[str]):
    write_lines(join(CONFIGURATION_DIRECTORY, constants.ERRORS), error_lines)
