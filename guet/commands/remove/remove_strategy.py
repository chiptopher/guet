from guet.commands.strategy import CommandStrategy
from guet.config.errors import InvalidInitialsError
from guet.context.context import Context


def _without_committer_with_initials(initials, all_committers):
    return list(filter(lambda committer: committer.initials != initials, all_committers))


class RemoveCommitterStrategy(CommandStrategy):
    def __init__(self, initials: str, context: Context):
        self._initials = initials
        self.context = context

    def apply(self):
        try:
            committer_to_be_removed = self.context.committers.by_initials(self._initials)
            self.context.committers.remove(committer_to_be_removed)
        except InvalidInitialsError:
            print(f'No committer exists with initials "{self._initials}"')
