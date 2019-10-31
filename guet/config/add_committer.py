from os.path import join
from typing import List

from guet import constants
from guet.config import configuration_directory

_COMMITTER_NOT_PRESENT = -1


def add_committer(initials: str, name: str, email: str) -> None:
    all_committers = _read_all_committers_from_file()
    _add_committer_to_committers(all_committers, initials, name, email)
    _write_committers_to_file(all_committers)


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


def _read_all_committers_from_file() -> List[str]:
    committers_file = open(join(configuration_directory, constants.COMMITTERS), 'r')
    all_lines = committers_file.readlines()
    committers_file.close()
    return all_lines


def _write_committers_to_file(committers: List[str]) -> None:
    committers_file = open(join(configuration_directory, constants.COMMITTERS), 'w')
    committers_file.writelines(committers)
    committers_file.close()
