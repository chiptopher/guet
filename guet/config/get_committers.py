from os.path import join
from typing import List

from guet import constants
from guet.config import CONFIGURATION_DIRECTORY
from guet.config.committer import Committer

_INITIALS_POSITION = 0
_NAME_POSITION = 1
_EMAIL_POSITION = 2


def get_committers() -> List[Committer]:
    committers_file = open(join(CONFIGURATION_DIRECTORY, constants.COMMITTERS), 'r')
    committers_lines = committers_file.readlines()
    committers_file.close()
    return [_convert_committer_line_to_committer(line) for line in committers_lines]


def _convert_committer_line_to_committer(committer_line: str) -> Committer:
    split = committer_line.rstrip().split(',')
    return Committer(split[_NAME_POSITION], split[_EMAIL_POSITION], split[_INITIALS_POSITION])
