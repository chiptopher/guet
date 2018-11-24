
import unittest
from unittest.mock import Mock

from guet.commands.command import Command
from guet.executor import Executor
from guet.factory import CommandFactory


class TestExecutor(unittest.TestCase):

    def test_init_loads_command_factory_by_default(self):

        executor = Executor()
        self.assertIsNotNone(executor._command_factory)

    def test_execute_loads_a_command_from_command_factory_and_executes_it(self):

        command = Command([])
        command.execute = Mock()
        command_factory = CommandFactory()
        command_factory.create = Mock(return_value=command)
        executor = Executor(command_factory)

        args = []
        executor.execute(args)
        command_factory.create.assert_called_with(args)
        command.execute.assert_called()
