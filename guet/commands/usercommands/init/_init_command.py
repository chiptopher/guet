from guet.commands._context_command import ContextCommand
from guet.config.errors import AlreadyInitializedError


class InitCommand(ContextCommand):
    def execute(self):
        try:
            self._context.initialize()
        except AlreadyInitializedError:
            print('Config folder already exists.')
