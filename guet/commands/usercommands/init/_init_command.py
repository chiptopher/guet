from guet.commands._context_command import ContextCommand


class InitCommand(ContextCommand):
    def execute(self):
        self._context.initialize()
