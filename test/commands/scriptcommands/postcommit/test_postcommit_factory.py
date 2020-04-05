from unittest import TestCase

from guet.commands.scriptcommands.postcommit.postcommit_factory import PostCommitFactory
from guet.commands.scriptcommands.postcommit.postcommit_strategy import PostCommitStrategy
from guet.settings.settings import Settings


class TestPostCommitFactory(TestCase):

    def test_returns_post_commit_strategy(self):
        factory = PostCommitFactory()
        command = factory.build([], Settings)

        self.assertIsInstance(command.strategy, PostCommitStrategy)

