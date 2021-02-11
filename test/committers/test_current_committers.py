from unittest import TestCase
from unittest.mock import Mock, patch

from guet.committers import CurrentCommitters
from guet.committers.committer import Committer


class TestCurrentCommitter(TestCase):
    @patch('guet.committers._current_committers.project_root')
    @patch('guet.committers._current_committers.set_current_committers')
    def test_set_sets_current_committers(self, set_current_committers, mock_project_root):
        to_set = [Committer('name', 'email', 'initials')]
        current = CurrentCommitters(Mock(), Mock())
        current.set(to_set)
        set_current_committers.assert_called_with(
            to_set, mock_project_root.return_value)

    @patch('guet.committers._current_committers.project_root')
    @patch('guet.committers._current_committers.set_current_committers')
    def test_set_passes_committers_to_observers(self, _1, _2):
        observer = Mock()
        to_set = [Committer('name', 'email', 'initials')]
        current = CurrentCommitters(Mock(), Mock())
        current.register_observer(observer)
        current.set(to_set)

        observer.on_new_committers.assert_called_with(to_set)

    @patch('guet.committers._current_committers.project_root')
    @patch('guet.committers._current_committers.initials_for_project')
    def test_get_gets_all_committers(self, mock_initials, mock_project_root):
        committer1 = Mock()
        committer2 = Mock()

        def mock_by_initials(initials):
            if initials == 'initials1':
                return committer1
            else:
                return committer2

        mock_committers = Mock()
        mock_committers.by_initials.side_effect = mock_by_initials

        mock_initials.return_value = ['initials1', 'initials2']
        current = CurrentCommitters(Mock(), mock_committers)

        result = current.get()

        self.assertEqual([committer1, committer2], result)
