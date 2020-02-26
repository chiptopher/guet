from typing import List

from guet.config.committer import Committer
from guet.context.author_observable import AuthorObservable
from test.context.errors import InvalidCommittersError


class Context(AuthorObservable):
    def __int__(self):
        pass

    def set_committers(self, committers: List[Committer]):
        if len(committers) > 0:
            self.notify_author_observer(committers[0])
        else:
            raise InvalidCommittersError()
