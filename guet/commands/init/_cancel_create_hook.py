from typing import List

from guet.steps.action import Action


class CancelCreateHooks(Action):

    def execute(self, args: List[str]):
        print('guet not started.')
