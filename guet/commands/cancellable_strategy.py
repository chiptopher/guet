from guet.commands.strategy import CommandStrategy


class CancelableCommandStrategy(CommandStrategy):
    def __init__(self, prompt: str, success_callback: CommandStrategy, cancel_callback: CommandStrategy):
        self.prompt = prompt
        self.success_callback = success_callback
        self.cancel_callback = cancel_callback

    def apply(self):
        print(self.prompt)
        answer = input()
        if answer == 'y':
            self.success_callback.apply()
        else:
            if answer != 'x':
                print('Given input invalid. Cancelling command.')
            self.cancel_callback.apply()
