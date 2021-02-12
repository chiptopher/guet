from typing import List


class Step:

    def __init__(self):
        self._next = None

    def do_play(self, args: List[str]):
        raise NotImplementedError()

    def play(self, args: List[str]):
        self.do_play(args)
        if self._next is not None:
            self._next.play(args)

    def next(self, next_step: "Step") -> "Step":
        if self._next is None:
            self._next = next_step
        else:
            self._next.next(next_step)
        return self
