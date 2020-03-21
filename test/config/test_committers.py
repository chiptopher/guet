from os.path import join
from unittest import TestCase
from unittest.mock import patch, call, Mock

from guet import constants
from guet.config import CONFIGURATION_DIRECTORY
from guet.config.committer import Committer
from guet.config.committers import Committers
from guet.config.errors import InvalidInitialsError

default_read_lines_side_effects = [[
    'initials1,name1,email1\n',
    'initials2,name2,email2\n'
], FileNotFoundError()]


@patch('guet.config.committers.read_lines', side_effect=default_read_lines_side_effects)
class TestCommitters(TestCase):
    @patch('guet.config.committers.set_committer_as_author')
    @patch('guet.config.committers.set_current_committers')
    def test_notify_of_committer_set_sets_current_committers(self, mock_set_current_committers, _1, _2):
        observer = Committers()
        committer1 = Committer(name='name1', email='email1', initials='initials1')
        committer2 = Committer(name='name2', email='email2', initials='initials2')
        observer.notify_of_committer_set([committer1, committer2])
        mock_set_current_committers.assert_called_with([committer1, committer2])

    @patch('guet.config.committers.set_committer_as_author')
    @patch('guet.config.committers.set_current_committers')
    def test_notify_of_committer_set_sets_first_committer_author(self, _1, mock_set_author, _2):
        observer = Committers()
        committer1 = Committer(name='name1', email='email1', initials='initials1')
        committer2 = Committer(name='name2', email='email2', initials='initials2')
        observer.notify_of_committer_set([committer1, committer2])
        mock_set_author.assert_called_with(committer1)

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

    @patch('guet.config.committers.add_committer')
    def test_add_saves_committer_in_list_of_all_committers(self,
                                                           mock_add_committer,
                                                           _1):
        committers = Committers()
        committer = Committer(name='name', email='email', initials='initials')
        committer.save = Mock()
        committers.add(committer)
        self.assertIn(committer, committers.all())

    @patch('guet.config.committers.write_lines')
    def test_remove_removes_committer_from_list_committers(self, mock_write_lines, mock_read_lines):
        mock_read_lines.side_effect = [[
            'initials,name,email\n'
        ], FileNotFoundError()]
        committers = Committers()
        committer = Committer(name='name', email='email', initials='initials')
        committers.remove(committer)
        self.assertListEqual([], committers.all())

    @patch('guet.config.committers.write_lines')
    def test_remove_writes_new_committers_to_file(self, mock_write_lines, mock_read_lines):
        committers = Committers()
        committer = Committer(name='name2', email='email2', initials='initials2')
        committers.remove(committer)
        mock_write_lines.assert_called_with(join(CONFIGURATION_DIRECTORY, constants.COMMITTERS), [
            'initials1,name1,email1',
        ])

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


something = [[
    'initials1,name1,email1\n',
    'initials2,name2,email2\n'
], [
    'initials1,othername1,otheremail1\n'
]]


@patch('guet.config.committers.read_lines', side_effect=something)
class TestCommittersWithLocal(TestCase):
    path_to_project_root = '/path/to/project/root'

    def test_loads_committers_from_global_file_and_local_file(self, mock_read_lines):
        Committers(path_to_project_root=self.path_to_project_root)
        mock_read_lines.assert_has_calls([
            call(join(CONFIGURATION_DIRECTORY, constants.COMMITTERS)),
            call(join(self.path_to_project_root, '.guet', constants.COMMITTERS))
        ])

    def test_local_committers_overwrite_global_committers_with_matching_initials(self, mock_read_lines):
        committers = Committers(path_to_project_root=self.path_to_project_root)
        local_committer1 = Committer(initials='initials1', name='othername1', email='otheremail1')
        global_commtter2 = Committer(initials='initials2', name='name2', email='email2')
        self.assertListEqual([local_committer1, global_commtter2], committers.all())
