
class CreateStrategy:
    def apply(self):
        raise NotImplementedError()


class DoCreateStrategy(CreateStrategy):
    def apply(self):
        return True


class DontCreateStrategy(CreateStrategy):
    def apply(self):
        return False
