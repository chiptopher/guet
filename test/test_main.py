
from guet.main import main
from unittest.mock import Mock
from guet.executor import Executor
import unittest


class TestMain(unittest.TestCase):

    def test_main_calls_executor_execute_with_system_arguments(self):

        import sys
        sys.argv = ['one', 'two']
        expected_args = ['two']

        mock_executor = Executor()
        mock_executor.execute = Mock()

        main(mock_executor)
        mock_executor.execute.assert_called_with(expected_args)

