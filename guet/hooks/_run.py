import sys

from guet.committers import Committers2 as Committers
from guet.committers import CommittersProxy, CurrentCommitters
from guet.files import FileSystem
from guet.git import Git
from guet.steps import Step
from guet.util import project_root

from ._commit_msg import CommitMsg
from ._post_commit import PostCommit
from ._pre_commit import PreCommit

file_system = FileSystem()
committers = CommittersProxy()
committers2 = Committers(file_system)
git = Git(project_root().joinpath('.git'))
current_committers = CurrentCommitters(file_system, committers)
current_committers.register_observer(git)


def run(hook: str):
    command = _choose_command(hook)
    if command:
        command.play([])


def _choose_command(hook: str) -> Step:
    if hook.endswith('pre-commit'):
        return PreCommit(committers)
    elif hook.endswith('post-commit'):
        return PostCommit(current_committers)
    elif hook.endswith('commit-msg'):
        return CommitMsg(current_committers, git)
