from guet.config.add_committer import add_committer
from guet.config.already_initialized import already_initialized
from .command import Command2


class AddUserCommand(Command2):

    def __init__(self, args):
        super().__init__(args)

    def execute_hook(self):
        if len(self.args) != 3:
            if len(self.args) > 3:
                print('Too many arguments.')
            else:
                print('Not enough arguments.')
                print('')
                print(self.help())
                print('')
        else:
            if already_initialized():
                add_committer(self.args[0], self.args[1], self.args[2])
            else:
                print('guet has not been initialized yet! Please do so by running the command "guet init".')

    def help(self):
        return 'usage: guet add <initials> <"name"> <email>'

    @classmethod
    def help_short(cls) -> str:
        return 'Add committer to the list of available committers'
