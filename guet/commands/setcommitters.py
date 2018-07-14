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

from .command import Command
from ..gateway import *


class SetCommittersCommand(Command):
    _REQUIRED_ARGS_IN_CORRECT_ORDER = ['set']

    def __init__(self,
                 args,
                 user_gateway: UserGateway = UserGateway(),
                 file_gateway: FileGateway = FileGateway()):
        super().__init__(args)
        self._user_gateway = user_gateway
        self._file_gateway = file_gateway

    def execute(self):
        committer_initials = self._args[1:]
        committers = []
        for committer_initial in committer_initials:
            committer = self._user_gateway.get_user(committer_initial)
            committers.append(CommitterInput(name=committer.name, email=committer.email))
        self._file_gateway.set_committers(committers)

    def help(self):
        pass

    @classmethod
    def get_short_help_message(cls):
        return 'Set the current committers'

    @classmethod
    def get_list_of_required_arguments_in_correct_order(cls):
        return cls._REQUIRED_ARGS_IN_CORRECT_ORDER
