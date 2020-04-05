from unittest import TestCase
from unittest.mock import Mock

from guet.config.committer import Committer

from guet.commands.scriptcommands.commitmsg.commitmsg_strategy import CommitMsgStrategy
from guet.context.context import Context


class TestCommitMsgStrategy(TestCase):

    def test_appends_current_committer_coauthored_lines_to_message_text(self):
        context: Context = Mock()
        context.committers = Mock()
        context.committers.current.return_value = [
            Committer('name1', 'email1', 'initials1'),
            Committer('name2', 'email2', 'initials2')
        ]
        context.git = Mock()
        context.git.commit_msg = [
            f'Commit message'
        ]

        strategy = CommitMsgStrategy(context)
        strategy.apply()

        self.assertEqual(context.git.commit_msg, [
            f'Commit message',
            '\n',
            f'Co-authored-by: name1 <email1>',
            f'Co-authored-by: name2 <email2>'
        ])

    def test_replace_already_present_co_authored_messages(self):
        context: Context = Mock()
        context.committers = Mock()
        context.committers.current.return_value = [
            Committer('name3', 'email3', 'initials3'),
            Committer('name4', 'email4', 'initials4')
        ]
        context.git = Mock()
        context.git.commit_msg = [
            f'Commit message',
            '\n',
            f'Co-authored-by: name1 <email1>',
            f'Co-authored-by: name2 <email2>'
        ]

        strategy = CommitMsgStrategy(context)
        strategy.apply()

        self.assertEqual(context.git.commit_msg, [
            f'Commit message',
            '\n',
            f'Co-authored-by: name3 <email3>',
            f'Co-authored-by: name4 <email4>'
        ])

    def test_doesnt_append_coauthored_lines_if_only_one_committer(self):
        context: Context = Mock()
        context.committers = Mock()
        context.committers.current.return_value = [
            Committer('name1', 'email1', 'initials1'),
        ]
        context.git = Mock()
        context.git.commit_msg = [
            f'Commit message'
        ]

        strategy = CommitMsgStrategy(context)
        strategy.apply()

        self.assertEqual(context.git.commit_msg, [
            f'Commit message',
        ])
