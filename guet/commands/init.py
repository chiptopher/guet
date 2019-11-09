from guet.config.already_initialized import already_initialized
from guet.config.initialize import initialize
from .command import Command2


class InitDataSourceCommand(Command2):

    def __init__(self, args):
        super().__init__(args, args_needed=False)

    def execute_hook(self):
        extra_arguments_given = len(self.args) > 0
        if extra_arguments_given:
            print('Invalid arguments.\n\n   {}'.format(self.help()))
        else:
            if not already_initialized():
                initialize()
            else:
                print('Config folder already exists.')

    def help(self):
        return ''

    @classmethod
    def help_short(cls) -> str:
        return 'Initialize guet for use'
