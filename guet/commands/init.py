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


class InitDataSourceCommand(Command):
    _REQUIRED_ARGS_IN_CORRECT_ORDER = ['init']

    def __init__(self,
                 args,
                 file_gateway: FileGateway = FileGateway(),
                 print_gateway: PrintGateway = PrintGateway()):
        super().__init__(args, print_gateway)
        self.file_gateway = file_gateway

    def execute(self):
        if len(self._args) != 1:
            self._print_gateway.print('Invalid arguments.\n\n   {}'.format(self.help()))
        else:
            if not self.file_gateway.path_exists():
                self.file_gateway.initialize()
            else:
                self._print_gateway.print('Config folder already exists.')

    def help(self):
        pass

    @classmethod
    def get_short_help_message(cls):
        return 'Initialize guet for use'

    @classmethod
    def get_list_of_required_arguments_in_correct_order(cls):
        return cls._REQUIRED_ARGS_IN_CORRECT_ORDER
