from os.path import join
from pathlib import Path
from unittest import TestCase
from unittest.mock import patch, call, Mock

from guet.committers._committers_set import CommittersSet
from guet.committers.local_committer import LocalCommitter

from guet import constants
from guet.config import CONFIGURATION_DIRECTORY
from guet.committers.committer import Committer
from guet.committers.committers import Committers
from guet.errors import InvalidInitialsError

default_read_lines_side_effects = [[
    'initials1,name1,email1\n',
    'initials2,name2,email2\n'
], FileNotFoundError()]


@patch('guet.committers.committers.read_lines', side_effect=default_read_lines_side_effects)
class TestNotifyOfCommitters(TestCase):
    @patch('guet.committers.committers.set_current_committers')
    def test_notify_of_committer_set_sets_current_committers(self, mock_set_current_committers, _2):
        observer = Committers(path_to_project_root=Path('/path/to/project/root'))
        committer1 = Committer(name='name1', email='email1', initials='initials1')
        committer2 = Committer(name='name2', email='email2', initials='initials2')
        observer.notify_of_committer_set([committer1, committer2])
        mock_set_current_committers.assert_called_with([committer1, committer2], Path('/path/to/project/root'))


@patch('guet.committers.committers.read_lines', side_effect=default_read_lines_side_effects)
class TestCommittersAll(TestCase):
    def test_all_property_reads_committers_from_file(self, mock_read_lines):
        mock_read_lines.return_value = [
            'initials1,name1,email1\n',
            'initials2,name2,email2\n'
        ]
        expected_committers = [
            Committer(name='name1', email='email1', initials='initials1'),
            Committer(name='name2', email='email2', initials='initials2')
        ]
        committers = Committers()
        actual = committers.all()
        self.assertListEqual(expected_committers, actual)


@patch('guet.committers.committers.all_committers_set')
@patch('guet.committers.committers.current_millis', return_value=1000000000)
@patch('guet.committers.committers.read_lines', side_effect=default_read_lines_side_effects)
class TestCommittersCurrent(TestCase):

    def test_current_only_returns_committers_that_are_currently_set(self, mock_read_lines, mock_current_millis,
                                                                    mock_all_current_set):
        mock_read_lines.side_effect = [[
            'initials1,name1,email1\n',
            'initials2,name2,email2\n'
        ], FileNotFoundError(), [
            'initials1,initials2,1000000000,/project1',
            'initials1,1000000000,/project2',
        ]]
        mock_all_current_set.return_value = [
            CommittersSet(['initials1', 'initials2'], 1000000000, Path('/project1')),
            CommittersSet(['initials1', 'initials2'], 1000000000, Path('/project2'))
        ]

        expected_committers = [
            Committer(name='name1', email='email1', initials='initials1'),
            Committer(name='name2', email='email2', initials='initials2')
        ]
        committers = Committers(path_to_project_root=Path('/project1'))
        actual = committers.current()
        self.assertListEqual(expected_committers, actual)

    def test_current_maintains_currently_set_order(self, mock_read_lines, mock_current_millis, mock_all_current_set):
        mock_all_current_set.return_value = [CommittersSet(['initials2', 'initials1'], 1000000000, Path('/project1'))]
        mock_read_lines.side_effect = [[
            'initials1,name1,email1\n',
            'initials2,name2,email2\n'
        ], FileNotFoundError()]

        expected_committers = [
            Committer(name='name2', email='email2', initials='initials2'),
            Committer(name='name1', email='email1', initials='initials1')
        ]
        committers = Committers(path_to_project_root=Path('/project1'))
        actual = committers.current()
        self.assertListEqual(expected_committers, actual)

    def test_current_returns_empty_list_when_no_committers_present(self, mock_read_lines, mock_current_millis,
                                                                   mock_all_current_set):
        mock_all_current_set.return_value = [CommittersSet(['initials1', 'initials2'], 1000000000, Path('/project1'))]
        mock_read_lines.side_effect = [[
            'initials1,name1,email1\n',
            'initials2,name2,email2\n'
        ], FileNotFoundError()]
        committers = Committers(path_to_project_root=Path('/other_project'))
        actual = committers.current()
        self.assertListEqual([], actual)

    def test_current_returns_empty_list_when_current_time_is_after_set_time(self, mock_read_lines, mock_current_millis,
                                                                            mock_all_current_set):
        current_time = 1000000000
        mock_current_millis.return_value = current_time
        set_time = current_time - 86400000 - 1
        mock_all_current_set.return_value = [CommittersSet(['initials1', 'initials2'], set_time, Path('/project1'))]
        mock_read_lines.side_effect = [[
            'initials1,name1,email1\n',
            'initials2,name2,email2\n'
        ], FileNotFoundError()]
        committers = Committers(path_to_project_root=Path('/project1/.git'))
        actual = committers.current()
        self.assertListEqual([], actual)


@patch('guet.committers.committers.read_lines', side_effect=default_read_lines_side_effects)
class TestCommittersAdd(TestCase):

    def test_add_writes_committer_to_file(self, _1):
        committers = Committers()
        committer = Committer(name='name', email='email', initials='initials')
        committer.save = Mock()
        committers.add(committer)
        committer.save.assert_called()

    def test_add_doesnt_write_committer_to_file_if_committer_already_present(self,
                                                                             mock_read_lines):
        mock_read_lines.side_effect = [[
            'initials,name,email\n',
        ], FileNotFoundError()]
        committers = Committers()
        committer = Committer(name='name', email='email', initials='initials')
        committer.save = Mock()
        committers.add(committer)
        committer.save.assert_not_called()

    def test_add_saves_committer_in_list_of_all_committers(self, _1):
        committers = Committers()
        committer = Committer(name='name', email='email', initials='initials')
        committer.save = Mock()
        committers.add(committer)
        self.assertIn(committer, committers.all())


@patch('guet.committers.committers.read_lines', side_effect=default_read_lines_side_effects)
class TestCommittersRemove(TestCase):

    @patch('guet.committers.committers.write_lines')
    def test_remove_removes_committer_from_list_committers(self, mock_write_lines, mock_read_lines):
        mock_read_lines.side_effect = [[
            'initials,name,email\n'
        ], FileNotFoundError()]
        committers = Committers()
        committer = Committer(name='name', email='email', initials='initials')
        committers.remove(committer)
        self.assertListEqual([], committers.all())

    @patch('guet.committers.committers.write_lines')
    def test_remove_writes_new_committers_to_file(self, mock_write_lines, mock_read_lines):
        committers = Committers()
        committer = Committer(name='name2', email='email2', initials='initials2')
        committers.remove(committer)
        mock_write_lines.assert_called_with(Path(join(CONFIGURATION_DIRECTORY, constants.COMMITTERS)), [
            'initials1,name1,email1',
        ])


@patch('guet.committers.committers.read_lines', side_effect=default_read_lines_side_effects)
class TestCommittersByInitials(TestCase):

    def test_by_initials_gets_committer_with_matching_initials(self, mock_read_lines):
        committers = Committers()
        found = committers.by_initials('initials2')
        self.assertEqual(Committer(name='name2', email='email2', initials='initials2'), found)

    def test_by_initials_raises_exception_when_asking_by_initials_that_dont_exist(self, mock_read_lines):
        committers = Committers()
        try:
            committers.by_initials('initials3')
            self.fail('Should raise exceotion')
        except InvalidInitialsError:
            pass


local_committers_with_match = [[
    'initials1,name1,email1\n',
    'initials2,name2,email2\n'
], [
    'initials1,othername1,otheremail1\n'
]]


@patch('guet.committers.committers.read_lines', side_effect=local_committers_with_match)
class TestCommittersWithLocal(TestCase):
    path_to_project_root = '/path/to/project/root'

    def test_loads_committers_from_global_file_and_local_file(self, mock_read_lines):
        Committers(path_to_project_root=Path(self.path_to_project_root))
        mock_read_lines.assert_has_calls([
            call(Path(join(CONFIGURATION_DIRECTORY, constants.COMMITTERS))),
            call(Path(join(self.path_to_project_root, '.guet', constants.COMMITTERS)))
        ])

    def test_local_committers_overwrite_global_committers_with_matching_initials(self, mock_read_lines):
        committers = Committers(path_to_project_root=Path(self.path_to_project_root))
        local_committer1 = Committer(initials='initials1', name='othername1', email='otheremail1')
        global_commtter2 = Committer(initials='initials2', name='name2', email='email2')
        self.assertListEqual([local_committer1, global_commtter2], committers.all())

    def test_doesnt_load_local_committers_if_no_project_root_passed(self, mock_read_lines):
        Committers()
        mock_read_lines.assert_called_once_with(Path(join(CONFIGURATION_DIRECTORY, constants.COMMITTERS)))

    def test_loads_local_committers_that_arent_in_global_committers(self, mock_read_lines):
        local_committers_with_match = [[
            'initials2,name2,email2\n'
        ], [
            'initials1,othername1,otheremail1\n'
        ]]
        mock_read_lines.side_effect = local_committers_with_match
        committers = Committers(path_to_project_root=Path(self.path_to_project_root))
        local_committer1 = Committer(initials='initials1', name='othername1', email='otheremail1')
        global_commtter2 = Committer(initials='initials2', name='name2', email='email2')
        self.assertListEqual([local_committer1, global_commtter2], committers.all())

    def test_add_with_replace_flag_removes_committer_with_matching_initials(self, mock_read_lines):
        default_read_lines_side_effects = [[
            'initials1,name1,email1\n',
            'initials2,name2,email2\n'
        ], FileNotFoundError()]
        mock_read_lines.side_effect = default_read_lines_side_effects
        committers = Committers(path_to_project_root=Path(self.path_to_project_root))
        committer_with_matching_initials = LocalCommitter(name='name1', email='email1', initials='initials1',
                                                          project_root=Path('path'))
        committer_with_matching_initials.save = Mock()
        committers.add(committer_with_matching_initials, replace=True)
        committer_with_matching_initials.save.assert_called()
