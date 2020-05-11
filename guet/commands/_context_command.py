from guet.context.context import Context

from guet.commands.command import Command


class ContextCommand(Command):

    def __init__(self, context: Context):
        self._context = context

    def execute(self):
        raise NotImplementedError
