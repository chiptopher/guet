from guet.steps.step import Step


class Preparation(Step):

    def __init__(self):
        super().__init__()

    def prepare(self):
        raise NotImplementedError()

    def do_play(self):
        self.prepare()
        self._next.do_play()
