from guet.config.committer import Committer
from guet.config.get_current_committers import get_current_committers
from guet.git.edit_commit_msg import edit_commit_msg


def _create_co_authored_line(committer: Committer):
    return f'Co-authored by: {committer.name} <{committer.email}>\n'


def commit_msg():
    current_committers = get_current_committers()
    co_authored_lines = [_create_co_authored_line(committer) for committer in current_committers]
    edit_commit_msg(co_authored_lines)
