from guet.commands.strategy import CommandStrategy


class DoNothingStrategy(CommandStrategy):
    def apply(self):
        pass
