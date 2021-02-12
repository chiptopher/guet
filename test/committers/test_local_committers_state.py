# pylint: disable=protected-access

from unittest import TestCase
from unittest.mock import Mock, patch

from guet.committers._global_committer_state import GlobalCommittersState
from guet.committers._local_committers_state import LocalCommittersState
from guet.committers.committer import Committer


class TestLocalCommittersState(TestCase):

    @patch('guet.committers._local_committers_state.project_root')
    def test_all_includes_all_local_committers_and_global_committers(self, _):
        committers_file = Mock()
        committers_file.read.return_value = [
            'initials2,name2,email2'
        ]
        file_system = Mock()
        file_system.get.return_value = committers_file

        global_state: GlobalCommittersState = Mock()
        global_committer = Committer('name1', 'email1', 'initial1')
        global_state.all = Mock(return_value=[global_committer])

        state = LocalCommittersState(file_system, global_state)

        result = state.all()

        local = Committer('name2', 'email2', 'initials2')
        self.assertEqual([global_committer, local], result)

    def test_all_gives_local_committers_precedence(self):
        file_system = Mock()

        global_state: GlobalCommittersState = Mock()
        committer = Committer('name1', 'email1', 'initials')
        global_state.all = Mock(return_value=[committer])

        local = Committer('name2', 'email2', 'initials')
        state = LocalCommittersState(file_system, global_state)
        state._all_local_committers = Mock(return_value=[local])

        result = state.all()

        self.assertEqual([local], result)

    def test_add_saves_new_committer_to_file(self):
        committers_file = Mock()
        file_system = Mock()
        file_system.get.return_value = committers_file

        found = Committer(initials='initials1', name='name1', email='email1')

        global_state: GlobalCommittersState = Mock()
        state = LocalCommittersState(file_system, global_state)
        state._all_local_committers = Mock(return_value=[found])
        state._local_committer_present = Mock(return_value=None)

        state.add(Committer('name2', 'email2', 'initials2'))

        committers_file.write.assert_called_with([
            'initials1,name1,email1',
            'initials2,name2,email2',
        ])

    def test_add_overwrites_commiter_with_same_initials(self):
        committers_file = Mock()
        file_system = Mock()
        file_system.get.return_value = committers_file

        found = Committer(initials='initials1', name='name1', email='email1')

        global_state: GlobalCommittersState = Mock()
        state = LocalCommittersState(file_system, global_state)
        state._all_local_committers = Mock(return_value=[found])

        state.remove = Mock()
        state.add(Committer('name2', 'email2', 'initials1'))

        state.remove.assert_called_with('initials1')

    @patch('builtins.print')
    def test_add_warns_when_local_committer_will_shadow_global_committer(self, mock_print):
        committers_file = Mock()
        file_system = Mock()
        file_system.get.return_value = committers_file

        found = Committer(initials='initials1', name='name1', email='email1')

        global_state: GlobalCommittersState = Mock()
        global_state.by_initials.return_value = found

        state = LocalCommittersState(file_system, global_state)
        state._all_local_committers = Mock(return_value=[])

        state.add(Committer('name2', 'email2', 'initials1'))

        mock_print.assert_called_with(('Adding committer with initials "initials1" will '
                                       'overshadow global committer with same initials.'))

    def test_remove_removes_committer(self):
        file_system = Mock()
        committers_file = Mock()
        file_system.get.return_value = committers_file

        found = Committer(initials='initials1', name='name1', email='email1')

        state = LocalCommittersState(file_system, Mock())
        state._all_local_committers = Mock(return_value=[found])

        state.remove('initials1')

        committers_file.write.assert_called_with([])
