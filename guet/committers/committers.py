from os.path import join
from typing import List, Union

from guet.util import current_millis

from guet import constants
from guet.committers.global_committer import GlobalCommitter
from guet.committers.local_committer import LocalCommitter
from guet.config import CONFIGURATION_DIRECTORY
from guet.committers.committer import Committer
from guet.errors import InvalidInitialsError
from guet.committers._set_current_committers import set_current_committers
from guet.context.set_committer_observer import SetCommitterObserver
from guet.files.read_lines import read_lines
from guet.files.write_lines import write_lines

_TWENTY_FOUR_HOURS_IN_MILLISECONDS = 86400000


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


def _current_initials(project_root: str) -> List[str]:
    lines = read_lines(join(CONFIGURATION_DIRECTORY, constants.COMMITTERS_SET))
    try:
        project_set_line = next(project_line for project_line in lines if project_line.endswith(project_root))
        *initials, set_time, _ = project_set_line.split(',')
        current_time = current_millis()
        if int(set_time) + _TWENTY_FOUR_HOURS_IN_MILLISECONDS < current_time:
            return []
        return initials
    except StopIteration:
        return []


def _replace_global_committers_with_local_committers_if_ids_match(global_committers: List[Committer],
                                                                  local_committers: List[Committer]):
    final = local_committers.copy()

    local_initials = [committer.initials for committer in local_committers]
    for committer in global_committers:
        if committer.initials not in local_initials:
            final.append(committer)

    return final


class Committers(SetCommitterObserver):
    def __init__(self, *, path_to_project_root: Union[str, None] = None):
        super().__init__()
        global_committers = _load_global_committers(join(CONFIGURATION_DIRECTORY, constants.COMMITTERS))
        local_committers = []
        try:
            if path_to_project_root is not None:
                local_committers = _load_local_committers(join(path_to_project_root, '.guet', constants.COMMITTERS),
                                                          path_to_project_root)
        except FileNotFoundError:
            pass
        final = _replace_global_committers_with_local_committers_if_ids_match(global_committers, local_committers)
        self._committers = final
        self.project_root = path_to_project_root

    def all(self):
        return self._committers

    def current(self) -> List[Committer]:
        current_initials = _current_initials(self.project_root)
        final = []
        for initials in current_initials:
            try:
                committer = next((committer for committer in self.all() if committer.initials == initials))
                final.append(committer)
            except StopIteration:
                pass
        return final

    def add(self, committer: Committer, *, replace: bool = False):
        if committer not in self.all() or replace:
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
        set_current_committers(new_committers, self.project_root)
