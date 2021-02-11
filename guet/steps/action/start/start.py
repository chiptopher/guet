from guet.settings.settings import Settings
from guet.steps.action.action import Action


class StartAction(Action):
    def __init__(self, factory):
        super().__init__()
        self._factory = factory

    def execute(self, args):
        command = self._factory.build(args, Settings())
        command.execute()
