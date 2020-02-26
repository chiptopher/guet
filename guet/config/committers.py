from typing import List

from guet.config.committer import Committer
from guet.config.set_author import set_committer_as_author
from guet.config.set_current_committers import set_current_committers
from guet.context.set_committer_observer import SetCommitterObserver


class Committers(SetCommitterObserver):
    def notify_of_committer_set(self, new_committers: List[Committer]):
        set_current_committers(new_committers)
        set_committer_as_author(new_committers[0])
