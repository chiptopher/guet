"""
Copyright 2018 Christopher M. Boyer

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

    http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.
"""
from guet.gateways.io import PrintGateway
from .command import Command
from guet.gateways.gateway import *


class AddUserCommand(Command):

    _REQUIRED_ARGS_IN_CORRECT_ORDER = ['add']

    def __init__(self,
                 args,
                 user_gateway: UserGateway = UserGateway(),
                 print_gateway: PrintGateway = PrintGateway()):
        super().__init__(args, print_gateway)
        self._user_gateway = user_gateway

    def execute(self):
        if len(self._args) != 4:
            if len(self._args) > 4:
                self._print_gateway.print('Too many arguments.')
            else:
                self._print_gateway.print('Not enough arguments.')
                self._print_gateway.print('')
                self._print_gateway.print(self.help())
                self._print_gateway.print('')
        else:
            self._user_gateway.add_user(self._args[1], self._args[2], self._args[3])

    def help(self):
        return 'usage: guet add <initials> <"name"> <email>'

    @classmethod
    def get_short_help_message(cls):
        return 'Add committer to the list of available committers'

    @classmethod
    def get_list_of_required_arguments_in_correct_order(cls):
        return cls._REQUIRED_ARGS_IN_CORRECT_ORDER
