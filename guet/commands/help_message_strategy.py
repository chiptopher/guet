from guet.commands.strategy import CommandStrategy


class HelpMessageStrategy(CommandStrategy):
    def __init__(self, help_message: str):
        self.help_message = help_message

    def apply(self):
        print(self.help_message)
