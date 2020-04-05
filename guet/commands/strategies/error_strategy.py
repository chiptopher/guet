from guet.commands.strategies.strategy import CommandStrategy


class ErrorStrategy(CommandStrategy):
    def __init__(self, error_message: str):
        self.error_message = error_message

    def apply(self):
        print(self.error_message)
        exit(1)
