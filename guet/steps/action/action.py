from typing import List

from guet.steps.step import Step


class Action(Step):

    def do_play(self, args: List[str]):
        self.execute(args)

    def execute(self, args: List[str]):
        raise NotImplementedError()
