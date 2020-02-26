from unittest import TestCase
from unittest.mock import Mock

from guet.config.committer import Committer
from guet.context.author_observable import AuthorObservable
from guet.context.author_observer import AuthorObserver


class TestAuthorObservable(TestCase):

    def test_init_with_no_observers(self):
        observable = AuthorObservable()
        self.assertListEqual([], observable.author_observers)

    def test_add_observer_adds_an_observer(self):
        observable = AuthorObservable()
        observer = Mock()
        observable.add_author_observer(observer)
        self.assertListEqual([observer], observable.author_observers)

    def test_remove_observer_removes_observer_given(self):
        observable = AuthorObservable()
        observer = Mock()
        observable.add_author_observer(observer)
        observable.remove_author_observer(observer)
        self.assertListEqual([], observable.author_observers)

    def test_notify_notifies_all_observers(self):
        observable = AuthorObservable()
        observer: AuthorObserver = Mock()
        observable.add_author_observer(observer)
        committer = Committer(name='name', email='email', initials='initials')
        observable.notify_author_observer(committer)
        observer.notify_of_author.assert_called_with(committer)
