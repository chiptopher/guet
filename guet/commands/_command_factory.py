from guet.steps import Step


class CommandFactory:

    def build(self) -> Step:
        raise NotImplementedError
