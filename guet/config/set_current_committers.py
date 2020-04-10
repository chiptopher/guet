import time
from os.path import join
from typing import List

from guet import constants
from guet.config import CONFIGURATION_DIRECTORY
from guet.committers.committer import Committer
from guet.files.write_lines import write_lines
from guet.files.read_lines import read_lines


def _all_committers_set_from_file() -> List[str]:
    return read_lines(join(CONFIGURATION_DIRECTORY, constants.COMMITTERS_SET))


def _format_committers_to_committers_set_format(committers: List[Committer], project_path: str) -> str:
    git_path = project_path
    current_time_in_millis = int(round(time.time() * 1000))
    committer_initials = ','.join([committer.initials for committer in committers])
    return committer_initials + f',{current_time_in_millis},{git_path}'


def _add_to_current_set_lines(current_set, formatted_set_committers_information, project_path: str):
    git_path = project_path
    line_with_git_path = next((line for line in current_set if line.endswith(git_path)), None)
    if line_with_git_path:
        index = current_set.index(line_with_git_path)
        current_set[index] = formatted_set_committers_information
    else:
        current_set.append(formatted_set_committers_information)


def set_current_committers(committers: List[Committer], project_path: str) -> None:
    path = join(CONFIGURATION_DIRECTORY, constants.COMMITTERS_SET)
    current_set = _all_committers_set_from_file()
    formatted_set_committers_information = _format_committers_to_committers_set_format(committers, project_path)
    _add_to_current_set_lines(current_set, formatted_set_committers_information, project_path)
    write_lines(path, current_set)
