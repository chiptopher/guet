from guet.commands.strategy import CommandStrategy


class TooFewArgsStrategy(CommandStrategy):
    def __init__(self, help_message):
        super().__init__()
        self._help_message = help_message

    def apply(self):
        print('Not enough arguments.')
        print('')
        print(self._help_message)
