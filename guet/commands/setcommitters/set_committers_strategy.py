from typing import List

from guet.commands.strategy import CommandStrategy
from guet.config.committer import filter_committers_with_initials, Committer
from guet.context.context import Context


class SetCommittersStrategy(CommandStrategy):

    def __init__(self, args: List[str], context: Context):
        self.args = args
        self.context = context

    def apply(self):
        committers = self.context.committers.all()
        committer_initials = self.args
        committers_to_set = filter_committers_with_initials(committers, committer_initials)

        correct_number_of_committers_present = len(committers_to_set) is len(committer_initials)

        if not correct_number_of_committers_present:
            for initials in committer_initials:
                if not self._committer_with_initials_present(committers, initials):
                    print(f"No committer exists with initials '{initials}'")
        else:
            self.context.set_committers(committers_to_set)

    def _committer_with_initials_present(self, committers: List[Committer], initials: str):
        committer_with_initial_present = False
        for committer in committers:
            if committer.initials == initials:
                committer_with_initial_present = True
        return committer_with_initial_present
