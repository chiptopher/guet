from os.path import join
from typing import List

from guet import constants
from guet.config import CONFIGURATION_DIRECTORY
from guet.config.add_committer import add_committer
from guet.config.committer import Committer
from guet.config.errors import InvalidInitialsError
from guet.config.set_author import set_committer_as_author
from guet.config.set_current_committers import set_current_committers
from guet.context.set_committer_observer import SetCommitterObserver
from guet.files.read_lines import read_lines
from guet.files.write_lines import write_lines


def _load_committers():
    lines = read_lines(join(CONFIGURATION_DIRECTORY, constants.COMMITTERS))
    committers = []
    for line in lines:
        initials, name, email = line.rstrip().split(',')
        committers.append(Committer(initials=initials, name=name, email=email))
    return committers


def _write_committers(committers: List[Committer]):
    write_lines(join(CONFIGURATION_DIRECTORY, constants.COMMITTERS), [str(committer) for committer in committers])


class Committers(SetCommitterObserver):
    def __init__(self):
        super().__init__()
        self._committers = _load_committers()

    def all(self):
        return self._committers

    def add(self, committer: Committer):
        if committer not in self.all():
            self._committers.append(committer)
            add_committer(committer.initials, committer.name, committer.email)

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
