from typing import List

from guet.committers.committer import Committer

from guet.context.context import Context

from guet.commands.strategies.strategy import CommandStrategy


def _rotate_first_committer_to_last_committer(current: List[Committer]) -> List[Committer]:
    first_committer = current.pop(0)
    current.append(first_committer)
    return current


class PostCommitStrategy(CommandStrategy):
    def __init__(self, context: Context):
        self.context = context

    def apply(self):
        current = self.context.committers.current()
        current = _rotate_first_committer_to_last_committer(current)
        self.context.set_committers(current)
