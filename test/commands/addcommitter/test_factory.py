from unittest import TestCase
from unittest.mock import patch

from guet.commands.addcommitter.factory import AddCommitterFactory
from guet.commands.cancellable_strategy import CancelableCommandStrategy
from guet.config.committer import Committer
from guet.settings.settings import Settings


@patch('guet.commands.addcommitter.factory.get_committers')
class TestAddCommitterFactory(TestCase):

    def test_returns_cancelable_strategy_if_given_initials_match_already_present_committer(self, get_committers):
        get_committers.return_value = [Committer(initials='initials', name='name', email='email')]
        subject = AddCommitterFactory()
        response = subject.build(['add', 'initials', 'name', 'email'], Settings())
        self.assertIsInstance(response.strategy, CancelableCommandStrategy)
