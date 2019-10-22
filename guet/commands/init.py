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
