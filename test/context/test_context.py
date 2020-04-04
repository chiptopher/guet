from unittest import TestCase
from unittest.mock import Mock, patch

from guet.config.committer import Committer
from guet.context.set_committer_observer import SetCommitterObserver
from guet.context.context import Context
from guet.context.errors import InvalidCommittersError
from guet.git.errors import NoGitPresentError


@patch('guet.context.context.Committers')
@patch('guet.context.context.Git')
class TestContext(TestCase):

    @patch('guet.context.context.project_root', return_value='/path/to/cwd')
    def test_instance_only_load_project_root_if_its_used(self, mock_project_root, _1, _2):
        instance: Context = Context.instance()
        self.assertIsNone(instance._project_root_directory)
        self.assertEqual(instance.project_root_directory, '/path/to/cwd')

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

    def test_git_prop_loads_the_git_object(self, mock_git, mock_committers):
        context = Context('path/to/project/root/')
        self.assertEqual(mock_git.return_value, context.git)
        self.assertIn(mock_git.return_value, context.current_committers_observer)

    def test_committers_prop_loads_the_committers_if_not_loaded_and_adds_as_observer(self, _1, mock_committers):
        context = Context('path/to/project/root/')
        self.assertEqual(mock_committers.return_value, context.committers)
        self.assertIn(context.committers, context.current_committers_observer)

    def test_set_committers_attempts_to_load_git_module_if_not_already_present(self, _1, _2):
        context = Context('path/to/project/root')
        context.set_committers([Mock()])
        self.assertIsNotNone(context._git)

    def test_init_doesnt_load_git_observer_if_git_not_present_when_ignore_git_flag_present(self, mock_git, _1):
        mock_git.side_effect = NoGitPresentError()
        context = Context('path/to/project/root/')
        self.assertNotIn(mock_git.return_value, context.current_committers_observer)

    def test_committers_loaded_with_project_root(self, _1, mock_committers):
        context = Context('path/to/project/root/')
        context.__getattribute__('committers')
        mock_committers.assert_called_with(path_to_project_root='path/to/project/root/')
