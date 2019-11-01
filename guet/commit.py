from typing import List

from guet.config.committer import Committer
from guet.config.get_current_committers import get_current_committers
from guet.config.most_recent_committers_set import most_recent_committers_set
from guet.config.set_author import set_committer_as_author
from guet.config.set_current_committers import set_current_committers
from guet.currentmillis import current_millis
from guet.git.set_author import configure_git_author


class PostCommitManager:

    def manage(self):
        committers = self._rotate_fist_commiter_to_last_committer(get_current_committers())
        set_committer_as_author(committers[0])
        set_current_committers(committers)
        configure_git_author(committers[0].name, committers[0].email)

    def _rotate_fist_commiter_to_last_committer(self, committers: List[Committer]):
        new_last_committer = committers.pop(0)
        committers.append(new_last_committer)
        return committers


class PreCommitManager:

    def manage(self):
        now = current_millis()
        twenty_four_hours = 86400000
        twenty_four_hours_ago = now - twenty_four_hours
        set_time = most_recent_committers_set()
        if set_time < twenty_four_hours_ago:
            print("\nYou have not reset pairs in over twenty four hours!\nPlease reset your pairs by using guet set and including your pairs' initials\n")
            exit(1)
        else:
            exit(0)
