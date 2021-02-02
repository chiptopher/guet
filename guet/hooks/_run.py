import sys

from guet.committers import CommittersProxy
from guet.git import Git
from guet.steps import Step
from guet.util import project_root

from._commit_msg import CommitMsg


def run(hook: str):
    command = _choose_command(hook)
    if command:
        command.play([])


def _choose_command(hook: str) -> Step:
    committers = CommittersProxy()
    git = Git(project_root().joinpath('.git'))
    if hook.endswith('pre-commit'):
        pass
    elif hook.endswith('post-commit'):
        pass
    elif hook.endswith('commit-msg'):
        return CommitMsg(committers, git)
