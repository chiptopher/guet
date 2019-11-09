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


class Command:
    def __init__(self, args):
        self._args = args

    def execute(self):
        raise NotImplementedError

    def help(self):
        raise NotImplementedError

    @classmethod
    def get_short_help_message(cls):
        raise NotImplementedError


class Command2(Command):
    @classmethod
    def get_short_help_message(cls):
        return cls.help_short()

    def __init__(self, args: List[str]):
        super().__init__(args)
        self.args = args[1:]

    def execute(self) -> None:
        if self._no_args_given():
            self._print_help_message()
        else:
            self.execute_hook()

    def execute_hook(self) -> None:
        raise NotImplementedError

    def help(self) -> str:
        raise NotImplementedError

    @classmethod
    def help_short(cls) -> str:
        raise NotImplementedError

    def _no_args_given(self) -> bool:
        return len(self.args) == 0

    def _print_help_message(self) -> None:
        print(f'{self.help()}\n')
