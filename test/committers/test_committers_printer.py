from unittest import TestCase
from unittest.mock import patch

from guet.committers import CommittersPrinter
from guet.committers.committer import Committer


@patch('builtins.print')
class TestCommittersPrinter(TestCase):

    def test_pretty_prints_committer_names(self, mock_print):
        committers = [
            Committer(name='Name1', initials='initials1', email='email1'),
            Committer(name='Name2', initials='initials2', email='email2')
        ]
        committers_printer = CommittersPrinter(initials_only=False)
        committers_printer.print(committers)

        mock_print.assert_any_call(committers[0].pretty())
        mock_print.assert_any_call(committers[1].pretty())

    def test_prints_committer_initials_only(self, mock_print):
        committers = [
            Committer(name='Name1', initials='initials1', email='email1'),
            Committer(name='Name2', initials='initials2', email='email2')
        ]
        committers_printer = CommittersPrinter(initials_only=True)
        committers_printer.print(committers)

        mock_print.assert_any_call('initials1, initials2')
