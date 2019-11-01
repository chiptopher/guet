import unittest
from os.path import join

from unittest.mock import patch

from guet import constants
from guet.config import configuration_directory
from guet.config.committer import Committer
from guet.config.get_current_committers import get_current_committers


@patch('guet.config.get_current_committers.get_committers')
class TestGetCurrentCommitters(unittest.TestCase):

    @patch('builtins.open', new_callable=unittest.mock.mock_open())
    def test_reads_committers_from_file_and_returns_committers(self,
                                                               mock_open,
                                                               mock_get_committers):
        mock_get_committers.return_value = [
            Committer('name0', 'email0', 'initials0'),
            Committer('name1', 'email1', 'initials1'),
            Committer('name2', 'email2', 'initials2')
        ]
        mock_open.return_value.readline.return_value = 'initials1,initials2,1000000000\n'

        committers = get_current_committers()
        self.assertEqual(committers[0].name, 'name1')
        self.assertEqual(committers[0].email, 'email1')
        self.assertEqual(committers[0].initials, 'initials1')
        self.assertEqual(committers[1].name, 'name2')
        self.assertEqual(committers[1].email, 'email2')
        self.assertEqual(committers[1].initials, 'initials2')

    @patch('builtins.open', new_callable=unittest.mock.mock_open())
    def test_reads_committers_from_file(self,
                                        mock_open,
                                        mock_get_committers):
        mock_open.return_value.readline.return_value = 'initials1,initials2,1000000000\n'
        get_current_committers()
        mock_open.assert_called_with(join(configuration_directory, constants.COMMITTERS_SET), 'r')

    @patch('builtins.open', new_callable=unittest.mock.mock_open())
    def test_get_current_committers_preserves_order_of_committers(self,
                                                                  mock_open,
                                                                  mock_get_committers):
        mock_get_committers.return_value = [
            Committer('name0', 'email0', 'initials0'),
            Committer('name1', 'email1', 'initials1'),
            Committer('name2', 'email2', 'initials2')
        ]
        mock_open.return_value.readline.return_value = 'initials2,initials1,1000000000\n'

        committers = get_current_committers()
        self.assertEqual(committers[0].name, 'name2')
        self.assertEqual(committers[0].email, 'email2')
        self.assertEqual(committers[0].initials, 'initials2')
        self.assertEqual(committers[1].name, 'name1')
        self.assertEqual(committers[1].email, 'email1')
        self.assertEqual(committers[1].initials, 'initials1')
