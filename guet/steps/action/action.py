from guet.steps.step import Step


class Action(Step):

    def do_play(self):
        self.execute()

    def execute(self):
        raise NotImplementedError()
