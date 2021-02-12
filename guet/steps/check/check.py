from typing import List

from guet.steps.step import Step


class Check(Step):
    def __init__(self, stop_message: str = None):
        super().__init__()
        self._stop_message = stop_message

    def do_play(self, args: List[str]):
        if self.should_stop(args):
            message = self._stop_message
            if message is None:
                message = self.load_message(args)
            print(message)
            exit(1)

    def should_stop(self, args: List[str]) -> bool:
        raise NotImplementedError()

    def load_message(self, _: List[str]) -> str:
        return ""
