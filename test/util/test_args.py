from unittest import TestCase

from guet.util import Args


class TestArgs(TestCase):
    def test_indexing_gets_result(self):
        args = Args(['one', 'two', 'three'])
        self.assertEqual('one', args[0])
        self.assertEqual('two', args[1])
        self.assertEqual('three', args[2])

    def test_without_flags_returns_args_without_flags(self):
        args = Args(['one', 'two', '--flag', 'three'])
        self.assertEqual('one', args.without_flags[0])
        self.assertEqual('two', args.without_flags[1])
        self.assertEqual('three', args.without_flags[2])
        self.assertEqual(3, len(args.without_flags))
