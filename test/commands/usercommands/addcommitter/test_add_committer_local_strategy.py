from os.path import join
from unittest import TestCase
from unittest.mock import Mock, patch

from guet.commands.usercommands.addcommitter.add_committer_locally_strategy import AddCommitterLocallyStrategy
from guet.committers.local_committer import LocalCommitter
from guet.committers.committers import Committers


@patch('guet.commands.usercommands.addcommitter.add_committer_locally_strategy.mkdir', return_value=True)
@patch('guet.commands.usercommands.addcommitter.add_committer_locally_strategy.isdir', return_value=True)
class TestAddLocalCommitterStrategy(TestCase):
    def test_apply_adds_committer_to_committers(self, mock_isdir, mock_mkdir):
        committers: Committers = Mock()
        strategy = AddCommitterLocallyStrategy('initials', 'name', 'email', '/path/to/root', committers)
        strategy.apply()

        expected = LocalCommitter(name='name', email='email', initials='initials', project_root='/path/to/root')
        committers.add.assert_called_with(expected, replace=True)

    def test_apply_creates_a_guet_directory_at_project_root_if_one_does_not_exist_already(self, mock_isdir, mock_mkdir):
        mock_isdir.return_value = False
        committers: Committers = Mock()
        strategy = AddCommitterLocallyStrategy('initials', 'name', 'email', '/path/to/root', committers)
        strategy.apply()

        mock_mkdir.assert_called_with(join('/path/to/root', '.guet'))
