import unittest
from unittest.mock import patch

from guet.hooks.pre_commit import pre_commit


@patch('guet.hooks.pre_commit.get_settings')
@patch('guet.hooks.pre_commit.PreCommitFactory')
class TestPostCommit(unittest.TestCase):

    def test_sets_committers_to_the_context(self,
                                            mock_pre_commit_factory,
                                            mock_get_settings):
        pre_commit()
        mock_pre_commit_factory.return_value.build.assert_called_with([], mock_get_settings.return_value)
        mock_command = mock_pre_commit_factory.return_value.build.return_value
        mock_command.execute.assert_called()
