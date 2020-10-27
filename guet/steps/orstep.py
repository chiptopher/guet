from typing import List, Callable
from guet.steps.step import Step


class OrStep(Step):
    def __init__(self, first: Step, second: Step, choice: Callable[[List[str]], bool]):
        self._first = first
        self._second = second
        self._choice = choice

    def do_play(self, args: List[str]):
        if self._choice(args):
            self._first.play(args)
        else:
            self._second.play(args)
