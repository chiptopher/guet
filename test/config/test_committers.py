from unittest import TestCase
from unittest.mock import patch

from guet.config.committer import Committer
from guet.config.committers import Committers

default_mock_read_lines_return_value = [
    'initials1,name1,email1\n',
    'initials2,name2,email2\n'
]


@patch('guet.config.committers.read_lines', return_value=default_mock_read_lines_return_value)
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

    @patch('guet.config.committers.add_committer')
    def test_add_writes_committer_to_file(self,
                                          mock_add_committer,
                                          _1):
        committers = Committers()
        committer = Committer(name='name', email='email', initials='initials')
        committers.add(committer)
        mock_add_committer.assert_called_with('initials', 'name', 'email')

    @patch('guet.config.committers.add_committer')
    def test_add_doesnt_write_committer_to_file_if_committer_already_present(self,
                                                                             mock_add_committer,
                                                                             mock_read_lines):
        mock_read_lines.return_value = [
            'initials,name,email\n',
        ]
        committers = Committers()
        committer = Committer(name='name', email='email', initials='initials')
        committers.add(committer)
        mock_add_committer.assert_not_called()

    @patch('guet.config.committers.add_committer')
    def test_add_saves_committer_in_list_of_all_committers(self,
                                                           mock_add_committer,
                                                           _1):
        committers = Committers()
        committer = Committer(name='name', email='email', initials='initials')
        committers.add(committer)
        self.assertIn(committer, committers.all())
