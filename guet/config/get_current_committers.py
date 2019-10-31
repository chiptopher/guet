from os.path import join
from typing import List

from guet import constants
from guet.config import configuration_directory
from guet.config.committer import Committer


def get_current_committers_names_and_emails() -> List[Committer]:
    f = open(join(configuration_directory, constants.COMMITTER_NAMES), 'r')
    lines = f.readlines()
    return [_extract_commiter_from_line_in_file(line) for line in lines]


def _extract_commiter_from_line_in_file(line: str) -> Committer:
    split = line.split(' ')
    name = ' '.join(split[:len(split) - 1])
    email = split[len(split) - 1].strip().strip('<').strip('>')
    return Committer(name, email)

