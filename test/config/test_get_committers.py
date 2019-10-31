import unittest
from os.path import join

from unittest.mock import patch

from guet import constants
from guet.config import configuration_directory
from guet.config.get_current_committers import get_current_committers_names_and_emails


class TestGetCommitters(unittest.TestCase):

    @patch('builtins.open', new_callable=unittest.mock.mock_open())
    def test_reads_committers_from_file(self, mock_open):
        mock_open.return_value.readlines.return_value = [
            'name1 <email1>\n',
            'name2 <email2>\n'
        ]
        committers = get_current_committers_names_and_emails()
        self.assertEqual(committers[0].name, 'name1')
        self.assertEqual(committers[0].email, 'email1')
        self.assertEqual(committers[1].name, 'name2')
        self.assertEqual(committers[1].email, 'email2')

    @patch('builtins.open', new_callable=unittest.mock.mock_open())
    def test_reads_committers_from_file(self, mock_open):
        mock_open.return_value.readlines.return_value = [
            'name1 <email1>\n',
            'name2 <email2>\n'
        ]
        get_current_committers_names_and_emails()
        mock_open.assert_called_with(join(configuration_directory, constants.COMMITTER_NAMES), 'r')
