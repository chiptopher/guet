from unittest import TestCase
from unittest.mock import Mock

from guet.committers._global_committer_state import GlobalCommittersState
from guet.committers.committer import Committer


class TestGlobalCommitersState(TestCase):
    def test_all_reads_all_committers_from_config_committers_file(self):
        file_system = Mock()
        committers_file = Mock()

        committers_file.read.return_value = [
            'initials1,name1,email1'
        ]

        file_system.get.return_value = committers_file

        state = GlobalCommittersState(file_system)
        result = state.all()
        self.assertEqual(result, [
            Committer(initials='initials1', name='name1', email='email1')
        ])

    def test_by_initials_finds_committer_with_given_initials(self):
        file_system = Mock()

        state = GlobalCommittersState(file_system)

        found = Committer(initials='initials1', name='name1', email='email1')
        state.all = Mock(return_value=[found])

        result = state.by_initials('initials1')
        self.assertEqual(result, found)

    def test_add_saves_new_committer_to_file(self):
        file_system = Mock()
        committers_file = Mock()
        file_system.get.return_value = committers_file

        found = Committer(initials='initials1', name='name1', email='email1')

        state = GlobalCommittersState(file_system)
        state.all = Mock(return_value=[found])

        state.add(Committer('name2', 'email2', 'initials2'))

        committers_file.write.assert_called_with([
            'initials1,name1,email1',
            'initials2,name2,email2',
        ])

    def test_add_overwrites_commiter_with_same_initials(self):
        file_system = Mock()
        committers_file = Mock()
        file_system.get.return_value = committers_file

        found = Committer(initials='initials1', name='name1', email='email1')

        state = GlobalCommittersState(file_system)
        state.all = Mock(return_value=[found])

        state.remove = Mock()
        state.add(Committer('name2', 'email2', 'initials1'))

        state.remove.assert_called_with('initials1')

    def test_remove_removes_committer(self):
        file_system = Mock()
        committers_file = Mock()
        file_system.get.return_value = committers_file

        found = Committer(initials='initials1', name='name1', email='email1')

        state = GlobalCommittersState(file_system)
        state.all = Mock(return_value=[found])

        state.remove('initials1')

        committers_file.write.assert_called_with([
        ])
