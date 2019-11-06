
import collections
import unittest

from guet.commands.command import *

test_case = collections.namedtuple('TestCase', 'input expected_output explanation')


def create_test_case(input, expected_output, explanation):
    return test_case(input=input, explanation=explanation, expected_output=expected_output)


class TestCommand(unittest.TestCase):

    def test_all_commands_pass_arguments_to_super_constructor(self):
        args = []
        for command_class in Command.__subclasses__():
            command = command_class(args)
            self.assertIsNotNone(command._args)


