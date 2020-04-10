from os.path import join
from typing import List

from guet import constants
from guet.config import CONFIGURATION_DIRECTORY

_COMMITTER_NOT_PRESENT = -1

_GLOBAL = join(CONFIGURATION_DIRECTORY, constants.COMMITTERS)


def add_committer(initials: str, name: str, email: str, *, file_path: str = _GLOBAL) -> None:
    all_committers = _read_all_committers_from_file(file_path)
    _add_committer_to_committers(all_committers, initials, name, email)
    _write_committers_to_file(all_committers, file_path)


def _add_committer_to_committers(all_committers: List[str], initials: str, name: str, email: str):
    committer_formatted = f'{initials},{name},{email}\n'
    committer_position = _position_of_committer_with_initials(all_committers, initials)
    if committer_position is _COMMITTER_NOT_PRESENT:
        all_committers.append(committer_formatted)
    else:
        all_committers[committer_position] = committer_formatted


def _position_of_committer_with_initials(all_committers: List[str], initials: str) -> int:
    for index, committer in enumerate(all_committers):
        if committer.startswith(initials):
            return index
    return _COMMITTER_NOT_PRESENT


def _read_all_committers_from_file(path) -> List[str]:
    try:
        committers_file = open(path, 'r')
        all_lines = committers_file.readlines()
        committers_file.close()
        return all_lines
    except FileNotFoundError:
        return []


def _write_committers_to_file(committers: List[str], path: str) -> None:
    committers_file = open(path, 'w')
    committers_file.writelines(committers)
    committers_file.close()
