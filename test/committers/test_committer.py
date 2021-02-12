from unittest import TestCase

from guet.committers.committer import Committer


class TestCommitter(TestCase):
    def test_initials_are_lower_case(self):
        committer = Committer(name='name', email='email', initials='INITIALS')
        self.assertEqual('initials', committer.initials)
