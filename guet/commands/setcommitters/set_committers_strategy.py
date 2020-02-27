from os import getcwd
from typing import List

from guet.commands.strategy import CommandStrategy
from guet.config.committer import filter_committers_with_initials, Committer
from guet.config.get_committers import get_committers
from guet.context.context import Context


class SetCommittersStrategy(CommandStrategy):

    def __init__(self, args: List[str]):
        self.args = args

    def apply(self):
        committers = get_committers()
        committer_initials = self.args
        committers_to_set = filter_committers_with_initials(committers, committer_initials)

        correct_number_of_committers_present = len(committers_to_set) is len(committer_initials)

        if not correct_number_of_committers_present:
            for initials in committer_initials:
                if not self._committer_with_initials_present(committers, initials):
                    print(f"No committer exists with initials '{initials}'")
        else:
            context = Context(getcwd())
            context.notify_set_committer_observers(committers_to_set)

    def _committer_with_initials_present(self, committers: List[Committer], initials: str):
        committer_with_initial_present = False
        for committer in committers:
            if committer.initials == initials:
                committer_with_initial_present = True
        return committer_with_initial_present
