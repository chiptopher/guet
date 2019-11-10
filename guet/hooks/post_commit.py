from typing import List

from guet.git.set_author import configure_git_author

from guet.config.committer import Committer
from guet.config.get_current_committers import get_current_committers
from guet.config.set_author import set_committer_as_author
from guet.config.set_current_committers import set_current_committers
from guet.util.errors import log_on_error


@log_on_error
def post_commit():
    committers = _rotate_fist_commiter_to_last_committer(get_current_committers())
    set_committer_as_author(committers[0])
    set_current_committers(committers)
    configure_git_author(committers[0].name, committers[0].email)


def _rotate_fist_commiter_to_last_committer(committers: List[Committer]):
    new_last_committer = committers.pop(0)
    committers.append(new_last_committer)
    return committers
