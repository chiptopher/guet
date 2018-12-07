import builtins
import sys

from guet.stdout_manager import StdoutManager


class InputGateway:

    def __init__(self, input_method=builtins.input):
        self._input_method = input_method

    def input(self):
        return self._input_method()


class PrintGateway:
    def __init__(self, stdout_manager=StdoutManager.get_instance()):
        self._stdout_manager = stdout_manager

    def print(self, text):
        original_stdout = sys.stdout
        sys.stdout = self._stdout_manager.get_stdout()
        print(text)
        sys.stdout = original_stdout
