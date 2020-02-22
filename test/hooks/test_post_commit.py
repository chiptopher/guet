import unittest
from unittest.mock import patch

from guet.config.committer import Committer
from guet.hooks.post_commit import post_commit


@patch('guet.hooks.post_commit.set_committer_as_author')
@patch('guet.hooks.post_commit.set_current_committers')
@patch('guet.hooks.post_commit.get_current_committers')
@patch('guet.hooks.post_commit.Git')
class TestPostCommit(unittest.TestCase):

    def test_manage_rotates_the_commit_names(self,
                                             mock_configure_git_author,
                                             mock_get_committers,
                                             mock_set_committers,
                                             mock_set_committer_as_author):
        committer1 = Committer(name='Name', email='email', initials='')
        committer2 = Committer(name='Name2', email='email', initials='')
        result = [committer1, committer2]

        mock_get_committers.return_value = result

        post_commit()

        mock_set_committers.assert_called_with([committer2, committer1])

    def test_manage_sets_the_new_author_name_and_email(self,
                                                       mock_configure_git_author,
                                                       mock_get_committers,
                                                       mock_set_committers,
                                                       mock_set_committer_as_author):
        committer1 = Committer(name='Name', email='email', initials='')
        committer2 = Committer(name='Name2', email='email', initials='')
        result = [committer1, committer2]
        mock_get_committers.return_value = result

        post_commit()

        mock_set_committer_as_author.assert_called_with(committer2)

    def test_manage_configures_git_to_use_new_author(self,
                                                     mock_git,
                                                     mock_get_committers,
                                                     mock_set_committers,
                                                     mock_set_committer_as_author):
        committer1 = Committer(name='Name', email='email', initials='')
        committer2 = Committer(name='Name2', email='email', initials='')
        result = [committer1, committer2]
        mock_get_committers.return_value = result

        post_commit()

        git = mock_git()
        self.assertEqual(git.author.name, committer2.name)
        self.assertEqual(git.author.email, committer2.email)
