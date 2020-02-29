import unittest
from unittest.mock import patch

from guet.config.committer import Committer
from guet.context.context import Context
from guet.hooks.post_commit import post_commit


@patch('guet.hooks.post_commit.Context')
@patch('guet.hooks.post_commit.get_current_committers')
class TestPostCommit(unittest.TestCase):

    def test_sets_committers_to_the_context(self,
                                            mock_get_committers,
                                            mock_context):
        committer1 = Committer(name='Name', email='email', initials='')
        committer2 = Committer(name='Name2', email='email', initials='')
        mock_get_committers.return_value = [committer1, committer2]
        context: Context = mock_context.return_value

        post_commit()

        context.set_committers.assert_called_with([committer2, committer1])
