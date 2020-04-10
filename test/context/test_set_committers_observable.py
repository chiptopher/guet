from unittest import TestCase
from unittest.mock import Mock

from guet.committers.committer import Committer
from guet.context.set_committers_observable import SetCommittersObservable
from guet.context.set_committer_observer import SetCommitterObserver


class TestAuthorObservable(TestCase):

    def test_init_with_no_observers(self):
        observable = SetCommittersObservable()
        self.assertListEqual([], observable.current_committers_observer)

    def test_add_observer_adds_an_observer(self):
        observable = SetCommittersObservable()
        observer = Mock()
        observable.add_set_committer_observer(observer)
        self.assertListEqual([observer], observable.current_committers_observer)

    def test_remove_observer_removes_observer_given(self):
        observable = SetCommittersObservable()
        observer = Mock()
        observable.add_set_committer_observer(observer)
        observable.remove_set_committer_observer(observer)
        self.assertListEqual([], observable.current_committers_observer)

    def test_notify_notifies_all_observers(self):
        observable = SetCommittersObservable()
        observer: SetCommitterObserver = Mock()
        observable.add_set_committer_observer(observer)
        committer = Committer(name='name', email='email', initials='initials')
        observable.notify_set_committer_observers([committer])
        observer.notify_of_committer_set.assert_called_with([committer])
