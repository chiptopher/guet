from os.path import join
from unittest import TestCase
from unittest.mock import patch, call

from guet import constants
from guet.config.committer import Committer
from guet.config.set_committers import set_committers
from guet.config import CONFIGURATION_DIRECTORY


@patch('guet.config.set_committers.add_committer')
@patch('guet.config.set_committers.write_lines')
class TestSetCommitters(TestCase):

    def test_writes_nothing_to_committers_file_to_clear_it(self, mock_write_lines, _mock1):
        set_committers([])
        mock_write_lines.assert_called_with(join(CONFIGURATION_DIRECTORY, constants.COMMITTERS), [])

    def test_adds_each_committer(self, _mock1, mock_add_committer):
        set_committers([Committer(name='name1', email='email1', initials='initials1'),
                        Committer(name='name2', email='email2', initials='initials2')])
        mock_add_committer.assert_has_calls([
            call('initials1', 'name1', 'email1'),
            call('initials2', 'name2', 'email2')
        ])
