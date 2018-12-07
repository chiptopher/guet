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


class Command:
    def __init__(self, args, print_gateway: PrintGateway = PrintGateway()):
        self._args = args
        self._print_gateway = print_gateway

    @classmethod
    def validate(cls, arguments: list):
        required_args = cls.get_list_of_required_arguments_in_correct_order()
        validated = len(arguments) >= len(required_args)
        for index, arg in enumerate(required_args):
            validated = validated and arg == arguments[index]
        return validated

    def execute(self):
        raise NotImplementedError

    def help(self):
        raise NotImplementedError

    @classmethod
    def get_short_help_message(cls):
        raise NotImplementedError

    @classmethod
    def get_list_of_required_arguments_in_correct_order(cls):
        raise NotImplementedError
