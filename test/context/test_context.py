from unittest import TestCase
from unittest.mock import Mock

from guet.config.committer import Committer
from guet.context.author_observer import AuthorObserver
from guet.context.context import Context
from test.context.errors import InvalidCommittersError


class TestContext(TestCase):

    def test_set_committers_notifies_author_observers_that_committer_in_first_position_is_author(self):
        context = Context()

        committer1 = Committer(name='name1', email='email1', initials='initials1')
        committer2 = Committer(name='name2', email='email2', initials='initials2')

        observer: AuthorObserver = Mock()
        context.add_author_observer(observer)

        context.set_committers([committer1, committer2])

        observer.notify_of_author.assert_called_with(committer1)

    def test_set_committers_raises_exception_when_given_an_empty_list(self):
        context = Context()

        observer: AuthorObserver = Mock()
        context.add_author_observer(observer)

        try:
            context.set_committers([])
            self.fail('Should raise exception')
        except InvalidCommittersError:
            pass
