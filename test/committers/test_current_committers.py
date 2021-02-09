from unittest import TestCase
from unittest.mock import Mock, patch

from guet.committers import CurrentCommitters
from guet.committers.committer import Committer


@patch('guet.committers._current_committers.project_root')
@patch('guet.committers._current_committers.set_current_committers')
class TestCurrentCommitter(TestCase):
    def test_set_sets_current_committers(self, set_current_committers, mock_project_root):
        to_set = [Committer('name', 'email', 'initials')]
        current = CurrentCommitters(Mock(), Mock())
        current.set(to_set)
        set_current_committers.assert_called_with(
            to_set, mock_project_root.return_value)

    def test_set_passes_committers_to_observers(self, _1, _2):
        observer = Mock()
        to_set = [Committer('name', 'email', 'initials')]
        current = CurrentCommitters(Mock(), Mock())
        current.register_observer(observer)
        current.set(to_set)

        observer.on_new_committers.assert_called_with(to_set)
