import datetime
from typing import List

from guet.config.committer import Committer
from guet.config.get_committers import get_committers
from guet.config.set_committers import set_committers
from guet.config.set_author import set_committer_as_author
from guet.gateways.gateway import PairSetGateway
from guet.gateways.io import PrintGateway
from guet.git.set_author import configure_git_author


class PostCommitManager:

    def manage(self):
        committers = self._rotate_fist_commiter_to_last_committer(get_committers())
        set_committer_as_author(committers[0])
        set_committers(committers)
        configure_git_author(committers[0].name, committers[0].email)

    def _rotate_fist_commiter_to_last_committer(self, committers: List[Committer]):
        new_last_committer = committers.pop(0)
        committers.append(new_last_committer)
        return committers


class PreCommitManager:

    def __init__(self, pair_set_gateway: PairSetGateway = PairSetGateway(),
                 print_gateway: PrintGateway = PrintGateway(), exit_method=exit):
        self._print_gateway = print_gateway
        self._pair_set_gateway = pair_set_gateway
        self._exit_method = exit_method

    def manage(self):
        now = round(datetime.datetime.utcnow().timestamp() * 1000)
        twenty_four_hours = 86400000
        twenty_four_hours_ago = now - twenty_four_hours
        if self._pair_set_gateway.get_most_recent_pair_set().set_time < twenty_four_hours_ago:
            self._print_gateway.print("\nYou have not reset pairs in over twenty four hours!\nPlease reset your pairs by using guet set and including your pairs' initials\n")
            self._exit_method(1)
        else:
            self._exit_method(0)
