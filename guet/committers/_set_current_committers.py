import time
from os.path import join
from pathlib import Path
from typing import List

from guet import constants
from guet.committers._committers_set import CommittersSet, all_committers_set
from guet.committers.committer import Committer
from guet.config import CONFIGURATION_DIRECTORY
from guet.files.write_lines import write_lines


def _format_committers_to_committers_set_format(committers: List[Committer],
                                                project_path: Path) -> CommittersSet:
    git_path = project_path
    current_time_in_millis = int(round(time.time() * 1000))
    committer_initials = [committer.initials for committer in committers]
    return CommittersSet(committer_initials, current_time_in_millis, git_path)


def _index_with_matching_path(current_set: List[CommittersSet],
                              formatted_set_committers_information: CommittersSet):
    for index, current in enumerate(current_set):
        if current.path == formatted_set_committers_information.path:
            return index
    return -1


def _add_to_current_set_lines(current_set: List[CommittersSet],
                              new_set: CommittersSet):
    index = _index_with_matching_path(current_set, new_set)
    if index != -1:
        _replace_committers_set_with_matching_initials(current_set, new_set, index)
    else:
        current_set.append(new_set)


def _replace_committers_set_with_matching_initials(current_committers_set: List[CommittersSet],
                                                   new_committers_set: CommittersSet,
                                                   index_of_match):
    current_committers_set[index_of_match] = new_committers_set


def _convert_to_text(current_set: CommittersSet) -> str:
    path = current_set.path
    current_time_in_millis = int(round(time.time() * 1000))
    committer_initials = ','.join(current_set.initials)
    return committer_initials + f',{current_time_in_millis},{path}'


def set_current_committers(committers: List[Committer], project_path: Path) -> None:
    path = Path(join(CONFIGURATION_DIRECTORY, constants.COMMITTERS_SET))
    current_set = all_committers_set()
    new_committers_set = _format_committers_to_committers_set_format(committers, project_path)
    _add_to_current_set_lines(current_set, new_committers_set)
    write_lines(path, [_convert_to_text(committers_set) for committers_set in current_set])
