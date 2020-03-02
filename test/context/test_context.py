from unittest import TestCase
from unittest.mock import Mock, patch

from guet.config.committer import Committer
from guet.context.set_committer_observer import SetCommitterObserver
from guet.context.context import Context
from guet.context.errors import InvalidCommittersError


@patch('guet.context.context.Committers')
@patch('guet.context.context.Git')
class TestContext(TestCase):
    @patch('guet.context.context.getcwd', return_value='/path/to/cwd')
    def test_instace_returns_instance_with_cwd_as_project_root(self, mock_getcwd, _1, _2):
        instance: Context = Context.instance()
        self.assertEqual(mock_getcwd.return_value, instance.project_root_directory)

    def test_set_committers_notifies_author_observers_that_committers_are_set(self, mock_git, mock_committers):
        context = Context('current/working/directory')

        committer1 = Committer(name='name1', email='email1', initials='initials1')
        committer2 = Committer(name='name2', email='email2', initials='initials2')

        observer: SetCommitterObserver = Mock()
        context.add_set_committer_observer(observer)

        context.set_committers([committer1, committer2])

        observer.notify_of_committer_set.assert_called_with([committer1, committer2])

    def test_set_committers_raises_exception_when_given_an_empty_list(self, mock_git, mock_committers):
        context = Context('current/working/directory/')

        observer: SetCommitterObserver = Mock()
        context.add_set_committer_observer(observer)

        try:
            context.set_committers([])
            self.fail('Should raise exception')
        except InvalidCommittersError:
            pass

    def test_init_loads_git_from_project_root_path_plus_git_directory(self, mock_git, mock_committers):
        Context('path/to/project/root/')
        mock_git.assert_called_with('path/to/project/root/.git')

    def test_loads_author_observers(self, mock_git, mock_committers):
        context = Context('path/to/project/root/')

        expected_author_observers = [mock_git.return_value, mock_committers.return_value]

        self.assertListEqual(expected_author_observers, context.current_committers_observer)
