import unittest
from unittest.mock import patch

from guet.config.get_committers import get_committers


class TestGetCommitters(unittest.TestCase):

    @patch('builtins.open', new_callabled=unittest.mock.mock_open())
    def test_reads_committers_from_file(self, mock_open):
        mock_open.return_value.readlines.return_value = [
            'initials1,name1,email1\n',
            'initials2,name2,email2\n'
        ]
        committers = get_committers()
        self.assertEqual('name1', committers[0].name)
        self.assertEqual('email1', committers[0].email)
        self.assertEqual('name2', committers[1].name)
        self.assertEqual('email2', committers[1].email)
