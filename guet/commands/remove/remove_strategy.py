from guet.commands.strategy import CommandStrategy
from guet.config.get_committers import get_committers
from guet.config.set_committers import set_committers


def _without_committer_with_initials(initials, all_committers):
    return list(filter(lambda committer: committer.initials != initials, all_committers))


class RemoveCommitterStrategy(CommandStrategy):
    def __init__(self, initials: str):
        self._initials = initials

    def apply(self):
        all_committers = get_committers()
        filtered_committers = _without_committer_with_initials(self._initials, all_committers)

        committer_was_removed = len(all_committers) == len(filtered_committers)

        if committer_was_removed:
            print(f'No committer exists with initials "{self._initials}"')
        else:
            set_committers(filtered_committers)
