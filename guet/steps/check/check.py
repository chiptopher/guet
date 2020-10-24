from typing import List

from guet.steps.step import Step


class Check(Step):
    def __init__(self, stop_message: str):
        super().__init__()
        self._stop_message = stop_message

    def do_play(self, args: List[str]):
        if not self.should_stop():
            self._next.play()
        else:
            print(self._stop_message)
            exit(1)

    def should_stop(self, args: List[str]) -> bool:
        raise NotImplementedError()
