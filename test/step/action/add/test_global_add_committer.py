import unittest
from pathlib import Path
from unittest.mock import Mock

from guet.committers.committers import Committers
from guet.committers.global_committer import GlobalCommitter
from guet.steps.action.add.global_add_committer import GlobalAddCommitter


class TestGlobalAddCommitter(unittest.TestCase):

    def test_execute_adds_local_committer_to_committers(self):
        root = Path('/path/to/project/root')
        committers: Committers = Mock()
        action = GlobalAddCommitter(committers)

        action.execute(['initials', 'name', 'email'])

        expected = GlobalCommitter(
            initials='initials', name='name', email='emai')

        committers.add.assert_called_with(expected)
