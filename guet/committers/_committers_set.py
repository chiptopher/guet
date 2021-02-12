from os.path import join
from pathlib import Path
from typing import List, NamedTuple

from guet import constants
from guet.config import CONFIGURATION_DIRECTORY
from guet.files.read_lines import read_lines

CommittersSet = NamedTuple('CommittersSet',
                           [('initials', List[str]), ('set_time', int), ('path', Path)])


def all_committers_set() -> List[CommittersSet]:
    lines = read_lines(Path(join(CONFIGURATION_DIRECTORY, constants.COMMITTERS_SET)))
    committers_sets = []
    for line in lines:
        *initials, set_time, path_as_str = line.split(',')
        committers_sets.append(CommittersSet(initials, set_time, Path(path_as_str)))
    return committers_sets
