from os.path import join
from typing import List

from guet import constants
from guet.config import CONFIGURATION_DIRECTORY
from guet.config.add_committer import add_committer
from guet.config.committer import Committer
from guet.config.set_author import set_committer_as_author
from guet.config.set_current_committers import set_current_committers
from guet.context.set_committer_observer import SetCommitterObserver
from guet.files.read_lines import read_lines


def _load_committers():
    lines = read_lines(join(CONFIGURATION_DIRECTORY, constants.COMMITTERS))
    committers = []
    for line in lines:
        initials, name, email = line.rstrip().split(',')
        committers.append(Committer(initials=initials, name=name, email=email))
    return committers


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

    def notify_of_committer_set(self, new_committers: List[Committer]):
        set_current_committers(new_committers)
        set_committer_as_author(new_committers[0])
