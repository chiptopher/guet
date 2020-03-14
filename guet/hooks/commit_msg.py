from typing import List

from guet.git.git import Git
from guet.git.git_path_from_cwd import git_path_from_cwd

from guet.config.committer import Committer
from guet.config.get_current_committers import get_current_committers
from guet.util.errors import log_on_error


def _create_co_authored_line(committer: Committer):
    return f'Co-authored-by: {committer.name} <{committer.email}>\n'


def _replace_already_present_co_authored_messages(commit_message: List[str],
                                                  co_authored_lines: List[str]):
    commit_message_without_co_authored = [
        line for line in commit_message if not line.startswith('Co-authored')
    ]
    _remove_trailing_newline(commit_message_without_co_authored)
    return commit_message_without_co_authored + ['\n'] + co_authored_lines


def _remove_trailing_newline(commit_message_without_co_authored):
    if commit_message_without_co_authored[len(commit_message_without_co_authored) - 1] == '\n':
        del commit_message_without_co_authored[len(commit_message_without_co_authored) - 1]


@log_on_error
def commit_msg():
    git_path = git_path_from_cwd()
    git = Git(git_path)
    commit_message = git.commit_msg
    current_committers = get_current_committers()
    if len(current_committers) > 1:
        co_authored_lines = [_create_co_authored_line(committer) for committer in current_committers]
        final_commit_message = _replace_already_present_co_authored_messages(
            commit_message, co_authored_lines)
        git.commit_msg = final_commit_message
