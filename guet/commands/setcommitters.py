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
from typing import List

from guet.config.committer import filter_committers_with_initials, Committer
from guet.config.get_committers import get_committers
from guet.config.set_author import set_committer_as_author
from guet.config.set_current_committers import set_current_committers as set_committers
from .command import Command


class SetCommittersCommand(Command):
    _REQUIRED_ARGS_IN_CORRECT_ORDER = ['set']

    def __init__(self,
                 args):
        super().__init__(args)

    def execute(self):
        committers = get_committers()
        committer_initials = self._args[1:]
        committers_to_set = filter_committers_with_initials(committers, committer_initials)

        correct_number_of_committers_present = len(committers_to_set) is len(committer_initials)

        if not correct_number_of_committers_present:
            for initials in committer_initials:
                committer_with_initial_present = False
                for committer in committers:
                    if committer.initials == initials:
                        committer_with_initial_present = True
                if not committer_with_initial_present:
                    print(f"No committer exists with initials '{initials}'")
        else:
            set_committer_as_author(committers_to_set[0])
            set_committers(committers_to_set)

    def help(self):
        pass

    @classmethod
    def get_short_help_message(cls):
        return 'Set the current committers'

    @classmethod
    def get_list_of_required_arguments_in_correct_order(cls):
        return cls._REQUIRED_ARGS_IN_CORRECT_ORDER
