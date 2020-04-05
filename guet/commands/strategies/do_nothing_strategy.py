from guet.commands.strategies.strategy import CommandStrategy


class DoNothingStrategy(CommandStrategy):
    def apply(self):
        pass
