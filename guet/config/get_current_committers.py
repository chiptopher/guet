from os.path import join
from typing import List

from guet import constants
from guet.config import CONFIGURATION_DIRECTORY
from guet.config.committer import Committer, filter_committers_with_initials
from guet.config.get_committers import get_committers
from guet.files.read_lines import read_lines
from guet.git.git_path_from_cwd import git_path_from_cwd

POSITION_OF_LAST_ELEMENT = -1


def _get_committer_with_initials(committers: List[Committer], initials: str) -> Committer:
    return next(committer for committer in committers if committer.initials == initials)


def _committers_in_order_of_initials(committers: List[Committer],
                                     committer_initials: List[str]) -> List[Committer]:
    return list(map(lambda initials: _get_committer_with_initials(committers, initials), committer_initials))


def _line_ending_with_git_path(lines: List[str]) -> str:
    git_path = git_path_from_cwd()
    return next((line for line in lines if line.endswith(git_path)), None)


def _process_lines_from_committer_set(lines: List[str]) -> List[Committer]:
    line = _line_ending_with_git_path(lines)
    if not line:
        return []
    *committer_initials, _, _ = line.split(',')
    committers = get_committers()
    committers_with_initials = filter_committers_with_initials(committers, committer_initials)
    return _committers_in_order_of_initials(committers_with_initials, committer_initials)


def get_current_committers() -> List[Committer]:
    path = join(CONFIGURATION_DIRECTORY, constants.COMMITTERS_SET)
    lines = read_lines(path)
    if len(lines) > 0:
        return _process_lines_from_committer_set(lines)
    else:
        return []
