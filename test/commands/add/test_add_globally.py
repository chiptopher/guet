from unittest import TestCase
from unittest.mock import Mock

from guet.commands.add._global_add import AddCommittersGlobally
from guet.committers import GlobalCommitter


class TestAddCommittersGlobally(TestCase):

    def test_adds_global_committer(self):
        committers = Mock()

        initials = 'initials'
        name = 'name'
        email = 'email'

        action = AddCommittersGlobally(committers)
        action.execute([initials, name, email])
        committers.add.assert_called_with(GlobalCommitter(name, email, initials))
