from guet.commands.strategies.strategy import CommandStrategy


class TooManyArgsStrategy(CommandStrategy):
    def apply(self):
        print('Too many arguments.')
