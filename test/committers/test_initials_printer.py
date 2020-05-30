from unittest import TestCase

from guet.committers import InitialsFormatter
from guet.committers.committer import Committer


class TestInitialsFormatter(TestCase):
    def test_prints_only_initials(self):
        committer1 = Committer('name', 'email', 'initials1')
        committer2 = Committer('name', 'email', 'initials2')
        self.assertEqual('initials1, initials2', str(InitialsFormatter([committer1, committer2])))
