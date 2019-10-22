
import builtins
import unittest
from guet.gateways.io import InputGateway
from unittest.mock import Mock


class TestInputGateway(unittest.TestCase):

    def test_input_gets_input_from_stdin(self):
        mock = Mock(return_value='text')
        input_gateway = InputGateway(mock)
        input = input_gateway.input()
        self.assertEqual('text', input)

    def test_input_method_defaults_to_builtin_print(self):
        input_gateway = InputGateway()
        input_gateway._input_method = builtins.input
