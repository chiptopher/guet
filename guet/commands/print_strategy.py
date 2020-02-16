from guet.commands.strategy import CommandStrategy


class PrintCommandStrategy(CommandStrategy):
    def __init__(self, text: str):
        self._text = text

    def apply(self):
        print(self._text)
