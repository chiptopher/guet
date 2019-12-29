from guet.commands.strategy import CommandStrategy


class TooManyArgsStrategy(CommandStrategy):
    def apply(self):
        print('Too many arguments.')
