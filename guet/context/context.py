from os.path import join
from typing import List

from guet.config.committer import Committer
from guet.context.author_observable import AuthorObservable
from guet.git.git import Git
from test.context.errors import InvalidCommittersError


class Context(AuthorObservable):
    def __init__(self, project_root_directory: str):
        super().__init__()
        git = Git(join(project_root_directory, '.git'))
        self.add_author_observer(git)

    def set_committers(self, committers: List[Committer]):
        if len(committers) > 0:
            self.notify_author_observer(committers[0])
        else:
            raise InvalidCommittersError()
