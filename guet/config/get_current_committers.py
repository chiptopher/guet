from os.path import join
from typing import List

from guet import constants
from guet.config import CONFIGURATION_DIRECTORY
from guet.config.committer import Committer, filter_committers_with_initials
from guet.config.get_committers import get_committers


def get_current_committers() -> List[Committer]:
    set_committers_file = open(join(CONFIGURATION_DIRECTORY, constants.COMMITTERS_SET), 'r')
    line = set_committers_file.readline()
    set_committers_file.close()
    committer_initials = line.rstrip().split(',')
    del committer_initials[-1]
    committers = get_committers()
    committers_with_initials = filter_committers_with_initials(committers, committer_initials)
    final = []
    for initials in committer_initials:
        for committer in committers_with_initials:
            if committer.initials == initials:
                final.append(committer)
    return final
