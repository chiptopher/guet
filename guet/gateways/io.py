import builtins
import sys

from guet.stdout_manager import StdoutManager


class InputGateway:

    def __init__(self, input_method=builtins.input):
        self._input_method = input_method

    def input(self):
        return self._input_method()
