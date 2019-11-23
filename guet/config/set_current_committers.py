import time
from os.path import join
from typing import List

from guet import constants
from guet.config import CONFIGURATION_DIRECTORY
from guet.config.committer import Committer


def set_current_committers(committers: List[Committer]) -> None:
    committers_set_file = open(join(CONFIGURATION_DIRECTORY, constants.COMMITTERS_SET), 'w')
    committers_set_file.write(_format_committers_to_committers_set_format(committers))
    committers_set_file.close()


def _format_committers_to_committers_set_format(committers: List[Committer]) -> str:
    current_time_in_millis = int(round(time.time() * 1000))
    committer_initials = ','.join([committer.initials for committer in committers])
    return committer_initials + f',{current_time_in_millis}\n'
