from guet.context.context import Context

from guet.commands._context_command import ContextCommand
from guet.errors import InvalidInitialsError


class RemoveCommand(ContextCommand):
    def __init__(self, context: Context, initials: str):
        super().__init__(context)
        self._initials = str.lower(initials)

    def execute(self):
        try:
            committer = self._context.committers.by_initials(self._initials)
            self._context.committers.remove(committer)
        except InvalidInitialsError:
            print(f'No committer exists with initials "{self._initials}"')
