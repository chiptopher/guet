import unittest
from unittest.mock import patch

from guet.hooks.post_commit import post_commit


@patch('guet.hooks.post_commit.get_config')
@patch('guet.hooks.post_commit.PostCommitFactory')
class TestPostCommit(unittest.TestCase):

    def test_sets_committers_to_the_context(self,
                                            mock_post_commit_factory,
                                            mock_get_config):
        post_commit()
        mock_post_commit_factory.return_value.build.assert_called_with([], mock_get_config.return_value)
        mock_command = mock_post_commit_factory.return_value.build.return_value
        mock_command.execute()
