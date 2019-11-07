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
from typing import Dict

from .command import Command
from ..util import get_command_subclasses


class HelpCommand(Command):

    _REQUIRED_ARGS_IN_CORRECT_ORDER = []

    def __init__(self, args, command_builder_map=None):
        super().__init__(args)
        if command_builder_map is None:
            command_builder_map = dict()
        self.command_builder_map = command_builder_map

    def execute(self):
        print(self.help())

    def help(self):
        help_message = 'usage: guet <command>\n'
        for key in self.command_builder_map:
            help_message += '\n   {} -- {}'.format(key, self.command_builder_map[key].get_short_help_message())
        return help_message + '\n'

    def get_short_help_message(self):
        pass

    @classmethod
    def get_list_of_required_arguments_in_correct_order(cls):
        return cls._REQUIRED_ARGS_IN_CORRECT_ORDER
