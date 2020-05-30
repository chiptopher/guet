from unittest import TestCase

from guet.committers._initials_name_email_printer import InitialsNameEmailPrintFormatter
from guet.committers.committer import Committer


class TestInitialsNameEmailPrintFormatter(TestCase):
    def test_prints_committer_information_in_proper_format(self):
        committer = Committer('name', 'email', 'initials')
        self.assertEqual('initials - name <email>', str(InitialsNameEmailPrintFormatter(committer)))
