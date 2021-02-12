from unittest import TestCase
from unittest.mock import Mock

from guet.commands.init._create_hooks_alongside import CreateHooksAlongside
from guet.git import Git


class TestCreateHooksAlongsideAction(TestCase):
    def test_execute_uses_git_to_create_hooks_alongside(self):
        git: Git = Mock()
        action = CreateHooksAlongside(git)

        action.execute([])

        git.create_hooks.assert_called_with(alongside=True)
