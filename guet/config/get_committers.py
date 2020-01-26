from os.path import join
from typing import List

from guet import constants
from guet.config import CONFIGURATION_DIRECTORY
from guet.config.committer import Committer


def get_committers() -> List[Committer]:
    committers_file = open(join(CONFIGURATION_DIRECTORY, constants.COMMITTERS), 'r')
    committers_lines = committers_file.readlines()
    committers_file.close()
    return [_convert_committer_line_to_committer(line) for line in committers_lines]


def _convert_committer_line_to_committer(committer_line: str) -> Committer:
    initials, name, email = committer_line.rstrip().split(',')
    return Committer(initials=initials, name=name, email=email)
