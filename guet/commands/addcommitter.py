
from .command import Command
from guet.gateways.gateway import *
from guet.config.add_committer import add_committer


class AddUserCommand(Command):

    _REQUIRED_ARGS_IN_CORRECT_ORDER = ['add']

    def __init__(self,
                 args,
                 user_gateway: UserGateway = UserGateway()):
        super().__init__(args)
        self._user_gateway = user_gateway

    def execute(self):
        if len(self._args) != 4:
            if len(self._args) > 4:
                print('Too many arguments.')
            else:
                print('Not enough arguments.')
                print('')
                print(self.help())
                print('')
        else:
            try:
                self._user_gateway.add_user(self._args[1], self._args[2], self._args[3])
                add_committer(self._args[1], self._args[2], self._args[3])
            except UninitializedError:
                print('guet has not been initialized yet! Please do so by running the command "guet init".')

    def help(self):
        return 'usage: guet add <initials> <"name"> <email>'

    @classmethod
    def get_short_help_message(cls):
        return 'Add committer to the list of available committers'

    @classmethod
    def get_list_of_required_arguments_in_correct_order(cls):
        return cls._REQUIRED_ARGS_IN_CORRECT_ORDER
