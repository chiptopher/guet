from typing import List

from guet.config.committer import Committer
from guet.context.set_committer_observer import SetCommitterObserver


class SetCommittersObservable:
    def __init__(self):
        self.current_committers_observer: List[SetCommitterObserver] = []

    def add_set_committer_observer(self, observer: SetCommitterObserver):
        self.current_committers_observer.append(observer)

    def remove_set_committer_observer(self, observer: SetCommitterObserver):
        self.current_committers_observer.remove(observer)

    def notify_set_committer_observers(self, committers: List[Committer]):
        for observer in self.current_committers_observer:
            observer.notify_of_committer_set(committers)
