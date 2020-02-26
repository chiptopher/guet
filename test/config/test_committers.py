from unittest import TestCase
from unittest.mock import patch

from guet.config.committer import Committer
from guet.config.committers import Committers


@patch('guet.config.committers.set_committer_as_author')
@patch('guet.config.committers.set_current_committers')
class TestCommitters(TestCase):
    def test_notify_of_committer_set_sets_current_committers(self, mock_set_current_committers, _1):
        observer = Committers()
        committer1 = Committer(name='name1', email='email1', initials='initials1')
        committer2 = Committer(name='name2', email='email2', initials='initials2')
        observer.notify_of_committer_set([committer1, committer2])
        mock_set_current_committers.assert_called_with([committer1, committer2])
        mock_set_current_committers.assert_called_with([committer1, committer2])

    def test_notify_of_committer_set_sets_first_committer_author(self, _1, mock_set_author):
        observer = Committers()
        committer1 = Committer(name='name1', email='email1', initials='initials1')
        committer2 = Committer(name='name2', email='email2', initials='initials2')
        observer.notify_of_committer_set([committer1, committer2])
        mock_set_author.assert_called_with(committer1)
