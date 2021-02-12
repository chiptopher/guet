from typing import List

from guet.steps.step import Step


class Preparation(Step):

    def prepare(self, args: List[str]):
        raise NotImplementedError()

    def do_play(self, args: List[str]):
        self.prepare(args)
