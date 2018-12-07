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
from ..util import get_command_subclasses


class HelpCommand(Command):

    _REQUIRED_ARGS_IN_CORRECT_ORDER = []

    def __init__(self, args, print_gateway: PrintGateway = PrintGateway()):
        super().__init__(args, print_gateway)
        self._print_gateway = print_gateway

    def execute(self):
        self._print_gateway.print(self.help())

    @classmethod
    def validate(cls, arguments: list):
        return False

    def help(self, command_classes_func=get_command_subclasses):
        command_classes = command_classes_func([HelpCommand])
        help_message = 'usage: guet <command>\n'
        for command_class in command_classes:
            args = ''
            for arg in command_class.get_list_of_required_arguments_in_correct_order():
                args += '{} '.format(arg)
            help_message += '\n   {}-- {}'.format(args, command_class.get_short_help_message())
        return help_message + '\n'

    def get_short_help_message(self):
        pass

    @classmethod
    def get_list_of_required_arguments_in_correct_order(cls):
        return cls._REQUIRED_ARGS_IN_CORRECT_ORDER
