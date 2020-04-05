from unittest import TestCase
from unittest.mock import patch

from guet.commands.strategies.error_strategy import ErrorStrategy


@patch('builtins.print')
@patch('builtins.exit')
class TestErrorStrategy(TestCase):
    def test_prints_message_then_exits(self, mock_exit, mock_print):
        text = 'Error message'
        strategy = ErrorStrategy(text)
        strategy.apply()
        mock_print.assert_called_with(text)
        mock_exit.assert_called_with(1)
