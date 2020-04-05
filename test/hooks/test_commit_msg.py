import unittest
from unittest.mock import patch

from guet.hooks.commit_msg import commit_msg


@patch('guet.hooks.commit_msg.get_config')
@patch('guet.hooks.commit_msg.CommitMsgFactory')
class TestPostCommit(unittest.TestCase):

    def test_sets_committers_to_the_context(self,
                                            mock_commit_msg_factory,
                                            mock_get_config):
        commit_msg()
        mock_commit_msg_factory.return_value.build.assert_called_with([], mock_get_config.return_value)
        mock_command = mock_commit_msg_factory.return_value.build.return_value
        mock_command.execute.assert_called()
