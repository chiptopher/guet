from os.path import join
from typing import List

from guet import constants
from guet.committers.global_committer import GlobalCommitter
from guet.committers.local_committer import LocalCommitter
from guet.config import CONFIGURATION_DIRECTORY
from guet.config.committer import Committer
from guet.config.errors import InvalidInitialsError
from guet.config.set_author import set_committer_as_author
from guet.config.set_current_committers import set_current_committers
from guet.context.set_committer_observer import SetCommitterObserver
from guet.files.read_lines import read_lines
from guet.files.write_lines import write_lines


def _load_global_committers(path: str) -> List[Committer]:
    lines = read_lines(path)
    committers = []
    for line in lines:
        initials, name, email = line.rstrip().split(',')
        committers.append(GlobalCommitter(initials=initials, name=name, email=email))
    return committers


def _load_local_committers(path: str, path_to_project_root: str) -> List[Committer]:
    lines = read_lines(path)
    committers = []
    for line in lines:
        initials, name, email = line.rstrip().split(',')
        committers.append(LocalCommitter(initials=initials, name=name, email=email, project_root=path_to_project_root))
    return committers


def _write_committers(committers: List[Committer]):
    write_lines(join(CONFIGURATION_DIRECTORY, constants.COMMITTERS), [str(committer) for committer in committers])


def _replace_global_committers_with_local_committers_if_ids_match(global_committers: List[Committer],
                                                                  local_committers: List[Committer]):
    final = []
    for committer in global_committers:
        try:
            matching_committer = next(local for local in local_committers if local.initials == committer.initials)
            final.append(matching_committer)
        except StopIteration:
            final.append(committer)
    return final


class Committers(SetCommitterObserver):
    def __init__(self, *, path_to_project_root: str = ''):
        super().__init__()
        global_committers = _load_global_committers(join(CONFIGURATION_DIRECTORY, constants.COMMITTERS))
        try:
            local_committers = _load_local_committers(join(path_to_project_root, '.guet', constants.COMMITTERS),
                                                      path_to_project_root)
        except FileNotFoundError:
            local_committers = []
        final = _replace_global_committers_with_local_committers_if_ids_match(global_committers, local_committers)
        self._committers = final

    def all(self):
        return self._committers

    def add(self, committer: Committer):
        if committer not in self.all():
            self._committers.append(committer)
            committer.save()

    def by_initials(self, initials: str):
        try:
            return next((committer for committer in self._committers if committer.initials == initials))
        except StopIteration:
            raise InvalidInitialsError()

    def remove(self, committer: Committer):
        self._committers.remove(committer)
        _write_committers(self._committers)

    def notify_of_committer_set(self, new_committers: List[Committer]):
        set_current_committers(new_committers)
        set_committer_as_author(new_committers[0])
