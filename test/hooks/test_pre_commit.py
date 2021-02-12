from unittest import TestCase
from unittest.mock import Mock, patch

from guet.hooks._pre_commit import PreCommit


@patch('builtins.print')
@patch('builtins.exit')
class TestPreCommit(TestCase):

    def test_execute_exits_if_no_committers_are_set(self, mock_exit, _):
        current = Mock()
        current.get = Mock(return_value=[])

        action = PreCommit(current)
        action.execute([])

        mock_exit.assert_called_with(1)

    def test_execute_prints_error_message(self, _, mock_print):
        current = Mock()
        current.get = Mock(return_value=[])

        action = PreCommit(current)
        action.execute([])

        mock_print.assert_called_with(
            'You must set your pairs before you can commit.')
