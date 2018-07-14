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

import unittest
from guet.commands.command import *
import collections


test_case = collections.namedtuple('TestCase', 'input expected_output explanation')


def create_test_case(input, expected_output, explanation):
    return test_case(input=input, explanation=explanation, expected_output=expected_output)


class CommandTest(unittest.TestCase):

    def _validate_test(self, case, command: Command):
        self.assertEqual(case.expected_output, command.validate(case.input), case.explanation)


class TestCommand(unittest.TestCase):

    def test_all_commands_pass_arguments_to_super_constructor(self):
        args = []
        for command_class in Command.__subclasses__():
            command = command_class(args)
            self.assertIsNotNone(command._args)


