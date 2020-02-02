from unittest import TestCase
from unittest.mock import patch, Mock, call

from guet.commands.cancellable_strategy import CancelableCommandStrategy

warning = 'warning'


@patch('builtins.print')
@patch('builtins.input', return_value='y')
class TestCancellableCommandStrategy(TestCase):

    def test_warning_printed(self, _, mock_print):
        strategy = CancelableCommandStrategy(warning, Mock(), Mock())
        strategy.apply()
        mock_print.assert_called_with(warning)

    def test_asks_user_for_input(self, mock_input, _):
        strategy = CancelableCommandStrategy(warning, Mock(), Mock())
        strategy.apply()
        mock_input.assert_called()

    def test_calls_success_callback_if_given_y(self, mock_input, _):
        mock_input.return_value = 'y'
        success_callback = Mock()
        strategy = CancelableCommandStrategy(warning, success_callback, Mock())
        strategy.apply()
        success_callback.apply.assert_called()

    def test_calls_cancel_callback_if_given_x(self, mock_input, _):
        mock_input.return_value = 'x'
        cancel_callback = Mock()
        strategy = CancelableCommandStrategy(warning, Mock(), cancel_callback)
        strategy.apply()
        cancel_callback.apply.assert_called()

    def test_giving_invalid_input_cancels_request_and_tells_user_they_gave_invalid_input(self, mock_input, mock_print):
        mock_input.return_value = 'other characters'
        cancel_callback = Mock()
        strategy = CancelableCommandStrategy(warning, Mock(), cancel_callback)
        strategy.apply()
        mock_print.assert_called_with('Given input invalid. Cancelling command.')
        cancel_callback.apply.assert_called()

    def test_giving_x_does_not_print_invalid_input_warning(self, mock_input, mock_print):
        mock_input.return_value = 'x'
        cancel_callback = Mock()
        strategy = CancelableCommandStrategy(warning, Mock(), cancel_callback)
        strategy.apply()
        mock_print.assert_called_with(warning)
