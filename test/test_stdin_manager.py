
import sys
import unittest
from guet.stdin_manager import StdinManager


class TestStdinManager(unittest.TestCase):

    def setUp(self):
        StdinManager._instance = None

    def test_init_sets_singleton_instance(self):
        self.assertIsNone(StdinManager._instance)
        stdin_manager = StdinManager()
        self.assertEqual(StdinManager._instance, stdin_manager)

    def test_init_sets_the_stdin_to_the_system_default(self):
        self.assertEqual(sys.__stdin__, StdinManager.get_instance().get_stdin())

    def test_set_stdin_sets_stdin(self):
        stdin_manager = StdinManager.get_instance()
        stdin = object()
        stdin_manager.set_stdin(stdin)
        self.assertEqual(stdin, stdin_manager.get_stdin())

