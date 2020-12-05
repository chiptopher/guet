from guet.steps import Step


class CommandFactory:

    def build() -> Step:
        raise NotImplementedError
