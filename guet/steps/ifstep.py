from typing import Callable, List

from guet.steps import Step


class IfStep(Step):
    def __init__(self, if_true: Callable[[List[str]], bool], steps: Step):
        super().__init__()
        self.if_true = if_true
        self.steps = steps

    def do_play(self, args: List[str]):
        if self.if_true(args):
            self.steps.play(args)
