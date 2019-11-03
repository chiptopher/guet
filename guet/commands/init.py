
from guet.config.already_initialized import already_initialized
from guet.config.initialize import initialize
from .command import Command


class InitDataSourceCommand(Command):
    _REQUIRED_ARGS_IN_CORRECT_ORDER = ['init']

    def __init__(self, args):
        super().__init__(args)

    def execute(self):
        if len(self._args) != 1:
            print('Invalid arguments.\n\n   {}'.format(self.help()))
        else:
            if not already_initialized():
                initialize()
            else:
                print('Config folder already exists.')

    def help(self):
        pass

    @classmethod
    def get_short_help_message(cls):
        return 'Initialize guet for use'

    @classmethod
    def get_list_of_required_arguments_in_correct_order(cls):
        return cls._REQUIRED_ARGS_IN_CORRECT_ORDER
