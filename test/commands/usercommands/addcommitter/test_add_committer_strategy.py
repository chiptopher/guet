from unittest import TestCase
from unittest.mock import Mock

from guet.commands.usercommands.addcommitter.add_committer_strategy import AddCommitterGloballyStrategy
from guet.committers.committer import Committer
from guet.committers.committers import Committers


class TestAddCommitterStrategy(TestCase):
    def test_apply_adds_committers(self):
        committers: Committers = Mock()
        strategy = AddCommitterGloballyStrategy('initials', 'name', 'email', committers)

        strategy.apply()

        committers.add.assert_called_with(Committer(initials='initials', name='name', email='email'))
