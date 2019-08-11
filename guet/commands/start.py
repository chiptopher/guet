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
from guet.gateways.io import PrintGateway, InputGateway
from guet.commands.command import Command
from guet.gateways.gateway import *


class StartCommand(Command):
    _REQUIRED_ARGS_IN_CORRECT_ORDER = ['start']

    def __init__(self,
                 args,
                 git_gateway: GitGateway = GitGateway(),
                 print_gateway: PrintGateway = PrintGateway(),
                 input_gateway: InputGateway = InputGateway()):
        super().__init__(args, print_gateway)
        self._input_gateway = input_gateway
        self._git_gateway = git_gateway

    def execute(self):
        if self._git_gateway.git_present():
            init_with_python3_shebang = False
            if '--python3' in self._args:
                init_with_python3_shebang = True
            if not self._git_gateway.any_hook_present():
                self._git_gateway.add_hooks(GitGateway.DEFAULT, init_with_python3_shebang)
            else:
                flag = None
                while not flag:
                    self._print_gateway.print('There is already commit hooks in this project. Would you like to overwrite (o), create (c) the file and put it in the hooks folder, or cancel (x)?')
                    val = self._input_gateway.input()
                    if val == 'o':
                        flag = GitGateway.OVERWRITE
                    elif val == 'c':
                        flag = GitGateway.CREATE_ALONGSIDE
                    elif val == 'x':
                        flag = GitGateway.CANCEL
                self._git_gateway.add_hooks(flag, init_with_python3_shebang)

        else:
            self._print_gateway.print('Git not initialized in this directory.')

    def help(self):
        pass

    @classmethod
    def get_short_help_message(cls):
        return 'Start guet usage in the repository at current directory'

    @classmethod
    def get_list_of_required_arguments_in_correct_order(cls):
        return cls._REQUIRED_ARGS_IN_CORRECT_ORDER
