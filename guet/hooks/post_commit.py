from os import getcwd
from typing import List

from guet.config.committer import Committer
from guet.config.get_current_committers import get_current_committers
from guet.context.context import Context
from guet.util.errors import log_on_error


@log_on_error
def post_commit():
    committers = _rotate_fist_commiter_to_last_committer(get_current_committers())
    context = Context(getcwd())
    context.set_committers(committers)


def _rotate_fist_commiter_to_last_committer(committers: List[Committer]):
    new_last_committer = committers.pop(0)
    committers.append(new_last_committer)
    return committers
