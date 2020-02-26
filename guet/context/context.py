from os.path import join
from typing import List

from guet.config.committer import Committer
from guet.config.committers import Committers
from guet.context.set_committers_observable import SetCommittersObservable
from guet.git.git import Git
from guet.context.errors import InvalidCommittersError


class Context(SetCommittersObservable):
    def __init__(self, project_root_directory: str):
        super().__init__()
        git = Git(join(project_root_directory, '.git'))
        committers = Committers()
        self.add_set_committer_observer(git)
        self.add_set_committer_observer(committers)

    def set_committers(self, committers: List[Committer]):
        if len(committers) > 0:
            self.notify_set_committer_observers(committers)
        else:
            raise InvalidCommittersError()
