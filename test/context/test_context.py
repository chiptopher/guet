from os.path import join
from pathlib import Path
from unittest import TestCase
from unittest.mock import Mock, patch, call
from guet import __version__

from guet.config import CONFIGURATION_DIRECTORY

from guet import constants
from guet.committers.committer import Committer
from guet.context.set_committer_observer import SetCommitterObserver
from guet.context.context import Context
from guet.context.errors import InvalidCommittersError
from guet.git.errors import NoGitPresentError


@patch('guet.context.context.Committers')
@patch('guet.context.context.Git')
class TestContext(TestCase):

    @patch('guet.context.context.project_root', return_value=Path('/path/to/cwd'))
    def test_instance_only_load_project_root_if_its_used(self, mock_project_root, _1, _2):
        instance: Context = Context.instance()
        self.assertIsNone(instance._project_root_directory)
        self.assertEqual(instance.project_root_directory, Path('/path/to/cwd').absolute())

    def test_set_committers_notifies_author_observers_that_committers_are_set(self, mock_git, mock_committers):
        context = Context(Path('current/working/directory'), file_system=Mock())

        committer1 = Committer(name='name1', email='email1', initials='initials1')
        committer2 = Committer(name='name2', email='email2', initials='initials2')

        observer: SetCommitterObserver = Mock()
        context.add_set_committer_observer(observer)

        context.set_committers([committer1, committer2])

        observer.notify_of_committer_set.assert_called_with([committer1, committer2])

    def test_set_committers_prints_names_of_committers_on_success(self, mock_git, mock_committers):
        context = Context(Path('current/working/directory'), file_system=Mock())

        committer1 = Committer(name='name1', email='email1', initials='initials1')
        committer2 = Committer(name='name2', email='email2', initials='initials2')

        observer: SetCommitterObserver = Mock()
        context.add_set_committer_observer(observer)

        context.set_committers([committer1, committer2])

        observer.notify_of_committer_set.assert_called_with([committer1, committer2])

    def test_set_committers_raises_exception_when_given_an_empty_list(self, mock_git, mock_committers):
        context = Context(Path('current/working/directory/'), file_system=Mock())

        observer: SetCommitterObserver = Mock()
        context.add_set_committer_observer(observer)

        try:
            context.set_committers([])
            self.fail('Should raise exception')
        except InvalidCommittersError:
            pass

    def test_git_prop_loads_the_git_object(self, mock_git, mock_committers):
        context = Context(Path('path/to/project/root/'), file_system=Mock())
        self.assertEqual(mock_git.return_value, context.git)
        self.assertIn(mock_git.return_value, context.current_committers_observer)

    def test_committers_prop_loads_the_committers_if_not_loaded_and_adds_as_observer(self, _1, mock_committers):
        context = Context(Path('path/to/project/root/'), file_system=Mock())
        self.assertEqual(mock_committers.return_value, context.committers)
        self.assertIn(context.committers, context.current_committers_observer)

    def test_set_committers_attempts_to_load_git_module_if_not_already_present(self, _1, _2):
        context = Context(Path('path/to/project/root'), file_system=Mock())
        context.set_committers([Mock()])
        self.assertIsNotNone(context._git)

    def test_init_doesnt_load_git_observer_if_git_not_present_when_ignore_git_flag_present(self, mock_git, _1):
        mock_git.side_effect = NoGitPresentError()
        context = Context(Path('path/to/project/root/'), file_system=Mock())
        self.assertNotIn(mock_git.return_value, context.current_committers_observer)

    def test_committers_loaded_with_project_root(self, _1, mock_committers):
        context = Context(Path('path/to/project/root/'), file_system=Mock())
        context.__getattribute__('committers')
        mock_committers.assert_called_with(path_to_project_root=Path('path/to/project/root/'))

    @patch('guet.context.context.project_root', side_effect=FileNotFoundError)
    def test_committers_loaded_without_root_path_if_none(self, mock_project_root, _1, mock_committers):
        context = Context(None, file_system=Mock())
        context.__getattribute__('committers')
        mock_committers.assert_called_with(path_to_project_root=None)


class TestContextInitialize(TestCase):

    def test_initialize_creates_appropriate_files(self):
        mock_file_system = Mock()
        context = Context(None, file_system=mock_file_system)

        context.initialize()

        mock_file_system.get.assert_has_calls([
            call(Path(join(CONFIGURATION_DIRECTORY, constants.COMMITTER_NAMES))),
            call(Path(join(CONFIGURATION_DIRECTORY, constants.COMMITTERS))),
            call(Path(join(CONFIGURATION_DIRECTORY, constants.COMMITTERS_SET))),
            call(Path(join(CONFIGURATION_DIRECTORY, constants.ERRORS))),
            call(Path(join(CONFIGURATION_DIRECTORY, constants.CONFIG))),
        ])
        mock_file_system.save_all.assert_called()

    def test_initialize_writes_version_to_config_file(self):
        mock_file_system = Mock()
        mock_file = Mock()
        mock_file_system.get = Mock(return_value=mock_file)

        context = Context(None, file_system=mock_file_system)

        context.initialize()

        mock_file.write.assert_called_with([f'{__version__}\n', '\n'])
