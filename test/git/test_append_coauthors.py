from unittest import TestCase

from guet.committers.committer import Committer
from guet.git._append_coauthors import append_committers


class TestAppendCoauthors(TestCase):
    def test_appends_current_committer_coauthored_lines_to_message_text(self):
        committer1 = Committer('name1', 'email1', 'initials1')
        committer2 = Committer('name2', 'email2', 'initials2')

        lines = [
            'Commit message'
        ]

        result = append_committers([committer1, committer2], lines)

        self.assertEqual([
            'Commit message',
            '',
            'Co-authored-by: name1 <email1>',
            'Co-authored-by: name2 <email2>'
        ], result)

    def test_replace_already_present_co_authored_messages(self):
        committer1 = Committer('name3', 'email3', 'initials3')
        committer2 = Committer('name4', 'email4', 'initials4')
        lines = [
            'Commit message',
            '',
            'Co-authored-by: name1 <email1>',
            'Co-authored-by: name2 <email2>'
        ]

        result = append_committers([committer1, committer2], lines)

        self.assertEqual([
            'Commit message',
            '',
            'Co-authored-by: name3 <email3>',
            'Co-authored-by: name4 <email4>'
        ], result)

    def test_doesnt_append_coauthored_lines_if_only_one_committer(self):
        committer1 = Committer('name1', 'email1', 'initials1')
        lines = ['Commit message']

        result = append_committers([committer1], lines)

        self.assertEqual(['Commit message'], result)
