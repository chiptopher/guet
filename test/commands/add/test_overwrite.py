from unittest import TestCase
from unittest.mock import Mock, patch

from guet.commands.add._overwrite import OverwritingCommitterCheck
from guet.committers.committer import Committer
from guet.errors import InvalidInitialsError


@patch('builtins.print', side_effect=['y'])
class TestOverwritingCommitterCheck(TestCase):

    @patch('builtins.input', side_effect=['y'])
    def test_prepare_prompts_user_for_input(self, mock_input, mock_print):
        committers = Mock()
        preparation = OverwritingCommitterCheck(committers)

        committer = Committer(initials='initials',
                              name='name1', email='email1')

        committers.by_initials.return_value = committer

        preparation.should_stop(['initials', 'name2', 'email2'])

        mock_print.assert_called_with(('Matching initials "initials". Adding '
                                       '"name2" <email2> will overwrite '
                                       '"name1" <email1>. Would you like '
                                       'to continue(y) or cancel(x)?'))

    @patch('builtins.input', side_effect=['x'])
    def test_should_stop_when_given_x_as_input(self, mock_input, mock_print):

        committers = Mock()
        preparation = OverwritingCommitterCheck(committers)

        committer = Committer(initials='initials',
                              name='name1', email='email1')

        committers.by_initials.return_value = committer

        self.assertTrue(preparation.should_stop(
            ['initials', 'name2', 'email2']))

    @patch('builtins.input', side_effect=['y'])
    def test_should_remove_overwritten_committer_if_given_y(self, mock_input,
                                                            mock_print):
        committers = Mock()
        preparation = OverwritingCommitterCheck(committers)

        committer = Committer(initials='initials',
                              name='name1', email='email1')

        committers.by_initials.return_value = committer

        preparation.should_stop(['initials', 'name2', 'email2'])

        committers.remove.assert_called_with(committer)

    @patch('builtins.input', side_effect=['y'])
    def test_overwriting_should_not_stop(self, mock_input, mock_print):
        committers = Mock()
        preparation = OverwritingCommitterCheck(committers)

        committer = Committer(initials='initials',
                              name='name1', email='email1')

        committers.by_initials.return_value = committer

        self.assertFalse(preparation.should_stop(
            ['initials', 'name2', 'email2']))

    @patch('builtins.input', side_effect=['y'])
    def test_not_finding_a_matching_committer_should_not_stop(self, mock_input,
                                                              mock_print):
        committers = Mock()
        preparation = OverwritingCommitterCheck(committers)

        committer = Committer(initials='initials',
                              name='name1', email='email1')

        committers.by_initials.side_effect = InvalidInitialsError()

        self.assertFalse(preparation.should_stop(
            ['initials', 'name2', 'email2']))
