from unittest import TestCase
from unittest.mock import Mock

from guet.commands.init._create_hooks_normally import CreateHooksNormally
from guet.git import Git


class TestCreateHooksNormally(TestCase):
    def test_execute_uses_git_to_create_hooks(self):
        git: Git = Mock()
        action = CreateHooksNormally(git)

        action.execute([])

        git.create_hooks.assert_called_with()
