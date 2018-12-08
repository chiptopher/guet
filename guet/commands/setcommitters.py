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


class SetCommittersCommand(Command):
    _REQUIRED_ARGS_IN_CORRECT_ORDER = ['set']

    def __init__(self,
                 args,
                 user_gateway: UserGateway = UserGateway(),
                 file_gateway: FileGateway = FileGateway(),
                 pair_set_gateway: PairSetGateway = PairSetGateway(),
                 pair_set_committers_gateway: PairSetGatewayCommitterGateway = PairSetGatewayCommitterGateway(),
                 print_gateway: PrintGateway = PrintGateway()):
        super().__init__(args)
        self._pair_set_committers_gateway = pair_set_committers_gateway
        self._pair_set_gateway = pair_set_gateway
        self._user_gateway = user_gateway
        self._file_gateway = file_gateway
        self._print_gateway = print_gateway

    def execute(self):
        committer_initials = self._args[1:]
        committers = []
        pair_set_id = self._pair_set_gateway.add_pair_set(round(datetime.datetime.utcnow().timestamp()*1000))
        pair_set_committer_add = []
        should_set_committers = self._prepare_pair_set_committers(committer_initials, committers, pair_set_committer_add)
        if should_set_committers:
            self._commit_pair_set_committers(committer_initials, committers, pair_set_committer_add, pair_set_id)

    def _commit_pair_set_committers(self, committer_initials, committers, pair_set_committer_add, pair_set_id):
            for pair_set_committer in pair_set_committer_add:
                initials = pair_set_committer
                id = pair_set_id
                self._pair_set_committers_gateway.add_pair_set_committer(initials, id)
            author = self._user_gateway.get_user(committer_initials[0])
            self._file_gateway.set_committers(committers)
            self._file_gateway.set_author_email(author.email)
            self._file_gateway.set_author_name(author.name)

    def _prepare_pair_set_committers(self, committer_initials: list, committers: list, pair_set_committer_add: list):
        should_set_committers = True
        for committer_initial in committer_initials:
            committer = self._user_gateway.get_user(committer_initial)
            if committer is None:
                self._print_gateway.print("No committer exists with initials '{}'".format(committer_initial))
                should_set_committers = False
                break
            committers.append(CommitterInput(name=committer.name, email=committer.email))
            pair_set_committer_add.append(committer_initial)
        return should_set_committers

    def help(self):
        pass

    @classmethod
    def get_short_help_message(cls):
        return 'Set the current committers'

    @classmethod
    def get_list_of_required_arguments_in_correct_order(cls):
        return cls._REQUIRED_ARGS_IN_CORRECT_ORDER
