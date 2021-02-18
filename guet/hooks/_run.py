from typing import Union

from guet.committers import Committers2 as Committers
from guet.committers import CurrentCommitters
from guet.files import FileSystem
from guet.git import Git
from guet.steps import Step
from guet.util import project_root

from ._commit_msg import CommitMsg
from ._post_commit import PostCommit
from ._pre_commit import PreCommit

FILE_SYSTEM = FileSystem()
COMMITTERS = Committers(FILE_SYSTEM)
GIT = Git(project_root().joinpath('.git'))
CURRENT_COMMITTERS = CurrentCommitters(FILE_SYSTEM, COMMITTERS)
CURRENT_COMMITTERS.register_observer(GIT)


def run(hook: str):
    command = _choose_command(hook)
    if command:
        command.play([])
    FILE_SYSTEM.save_all()


def _choose_command(hook: str) -> Union[Step, None]:
    if hook.endswith('pre-commit'):
        return PreCommit(CURRENT_COMMITTERS)
    elif hook.endswith('post-commit'):
        return PostCommit(CURRENT_COMMITTERS)
    elif hook.endswith('commit-msg'):
        return CommitMsg(CURRENT_COMMITTERS, GIT)
    return None
