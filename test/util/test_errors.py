import unittest
from unittest.mock import patch, Mock

from guet.util.errors import log_on_error


@patch('builtins.print')
@patch('guet.util.errors.set_errors')
@patch('traceback.format_exc')
class TestErrorWrapper(unittest.TestCase):
    def test_writes_to_error_file_when_something_goes_wrong(self,
                                                            mock_format_exc,
                                                            mock_set_errors,
                                                            mock_print):
        @log_on_error
        def func():
            raise ValueError

        mock_format_exc.return_value = [
            'line1\n'
        ]

        func()

        mock_set_errors.assert_called_with(['line1\n'])

    def test_says_an_error_occurred(self,
                                    mock_format_exc,
                                    mock_set_errors,
                                    mock_print):
        @log_on_error
        def func():
            raise ValueError

        mock_format_exc.return_value = [
            'line1\n'
        ]

        func()

        mock_print.assert_called_with('An error has occurred, please refer to error logs for more information\n')
