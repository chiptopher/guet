from typing import List

from guet.committers.committer import Committer


def _co_authored_lines(committers: List[Committer]) -> List[str]:
    return [f'Co-authored-by: {committer.name} <{committer.email}>' for committer in committers]


def _remove_co_authored_lines(old_message: List[str]) -> List[str]:
    return [line for line in old_message if not line.startswith('Co-authored-by: ')]


def _add_newline_if_necessary(without_co_authored_lines: List[str]) -> List[str]:
    if not without_co_authored_lines[len(without_co_authored_lines) - 1] == '':
        without_co_authored_lines.append('')
    return without_co_authored_lines


def _append_new_co_authored_lines(old_message: List[str], new_lines: List[str]) -> List[str]:
    without_co_authored_lines = _remove_co_authored_lines(old_message)
    with_newline = _add_newline_if_necessary(without_co_authored_lines)
    return with_newline + new_lines


def append_committers(committers: List[Committer], lines: List[str]) -> List[str]:
    if len(committers) > 1:
        return _append_new_co_authored_lines(lines, _co_authored_lines(committers))
    else:
        return lines
