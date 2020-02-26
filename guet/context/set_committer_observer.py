from typing import List

from guet.config.committer import Committer


class SetCommitterObserver:

    def __init__(self):
        pass

    def notify_of_committer_set(self, new_committers: List[Committer]):
        raise NotImplementedError()
