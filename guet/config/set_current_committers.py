import time
from os.path import join
from typing import List

from guet import constants
from guet.config import CONFIGURATION_DIRECTORY
from guet.config.committer import Committer
from guet.files.write_lines import write_lines
from guet.files.read_lines import read_lines
from guet.git.git_path_from_cwd import git_path_from_cwd


def set_current_committers(committers: List[Committer]) -> None:
    path = join(CONFIGURATION_DIRECTORY, constants.COMMITTERS_SET)
    lines = [_format_committers_to_committers_set_format(committers)]
    write_lines(path, lines)


def _format_committers_to_committers_set_format(committers: List[Committer]) -> str:
    git_path = git_path_from_cwd()
    current_time_in_millis = int(round(time.time() * 1000))
    committer_initials = ','.join([committer.initials for committer in committers])
    return committer_initials + f',{current_time_in_millis},{git_path}\n'
