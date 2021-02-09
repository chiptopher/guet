from unittest import TestCase
from unittest.mock import Mock, patch

from guet.committers.committer import Committer
from guet.committers._committers2 import Committers


class TestCommitters(TestCase):

    def test_initialized_with_global_state_as_current_state(self):
        file_system = Mock()
        committers = Committers(file_system)
        self.assertEqual(committers.current_state, committers.global_state)

    def test_to_local_switches_state_to_local(self):
        file_system = Mock()
        committers = Committers(file_system)
        committers.to_local()
        self.assertEqual(committers.current_state, committers.local_state)

    def test_to_global_switches_state_to_global(self):
        file_system = Mock()
        committers = Committers(file_system)
        committers.to_local()
        committers.to_global()
        self.assertEqual(committers.current_state, committers.global_state)

    def test_all_sorts_committers_alphabetically_by_initials(self):
        mock_state = Mock()

        second = Committer('name1', 'email1', 'z')
        first = Committer('name2', 'email2', 'a')

        mock_state.all.return_value = [second, first]

        committers = Committers(Mock())
        committers.current_state = mock_state
        found = committers.all()

        self.assertEqual(found, [first, second])
