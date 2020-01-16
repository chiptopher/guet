from os.path import join
from typing import List

from guet import constants
from guet.config import CONFIGURATION_DIRECTORY
from guet.config.committer import Committer, filter_committers_with_initials
from guet.config.get_committers import get_committers

POSITION_OF_LAST_ELEMENT = -1


def _get_committer_with_initials(committers: List[Committer], initials: str) -> Committer:
    return next(filter(lambda committer: committer.initials == initials, committers))


def _committers_in_order_of_initials(committers: List[Committer],
                                     committer_initials: List[str]) -> List[Committer]:
    return list(map(lambda initials: _get_committer_with_initials(committers, initials), committer_initials))


def get_current_committers() -> List[Committer]:
    set_committers_file = open(join(CONFIGURATION_DIRECTORY, constants.COMMITTERS_SET), 'r')
    line = set_committers_file.readline()
    set_committers_file.close()
    committer_initials = line.rstrip().split(',')
    del committer_initials[POSITION_OF_LAST_ELEMENT]
    committers = get_committers()
    committers_with_initials = filter_committers_with_initials(committers, committer_initials)
    return _committers_in_order_of_initials(committers_with_initials, committer_initials)
