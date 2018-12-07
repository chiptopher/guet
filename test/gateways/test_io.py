
from io import StringIO
import builtins
import sys
import unittest
from guet.gateways.io import PrintGateway, InputGateway
from guet.stdout_manager import StdoutManager
from unittest.mock import Mock


class TestPrintGateway(unittest.TestCase):

    def setUp(self):
        self.original_stdout = sys.stdout

    def tearDown(self):
        sys.stdout = self.original_stdout

    def test_init_set_the_stdout_as_the_default_system_stdout(self):
        print_gateway = PrintGateway()
        self.assertEqual(StdoutManager.get_instance(), print_gateway._stdout_manager)

    def test_print_writes_to_stdout(self):
        stdout = StringIO()
        stdout_manager = StdoutManager.get_instance()
        stdout_manager.set_stdout(stdout)
        print_gateway = PrintGateway(stdout_manager)
        text = 'text'
        print_gateway.print(text)
        self.assertEqual(text + '\n', stdout.getvalue())


class TestInputGateway(unittest.TestCase):

    def test_input_gets_input_from_stdin(self):
        mock = Mock(return_value='text')
        input_gateway = InputGateway(mock)
        input = input_gateway.input()
        self.assertEqual('text', input)

    def test_input_method_defaults_to_builtin_print(self):
        input_gateway = InputGateway()
        input_gateway._input_method = builtins.input
