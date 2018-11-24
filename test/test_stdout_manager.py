
import unittest

from guet.stdout_manager import StdoutManager


class TestStdoutManager(unittest.TestCase):

    def setUp(self):
        StdoutManager._instance = None

    def test_init_sets_singleton_instance(self):
        self.assertIsNone(StdoutManager._instance)
        stdout_manager = StdoutManager()
        self.assertEqual(stdout_manager, StdoutManager._instance)

    def test_init_sets_the_current_stdout_as_system_default(self):
        import sys
        self.assertEqual(sys.__stdout__, StdoutManager()._stdout)

    def test_get_instance_initializes_instance_if_there_is_none(self):
        StdoutManager.get_instance()
        self.assertIsNotNone(StdoutManager._instance)

    def test_get_instance_gets_the_singleton_instance(self):
        stdout_manager = StdoutManager.get_instance()
        self.assertEqual(StdoutManager._instance, stdout_manager)

    def test_get_instance_does_not_overwrite_singleton_instace_if_it_exists(self):
        stdout_manager1 = StdoutManager.get_instance()
        stdout_manager2 = StdoutManager.get_instance()
        self.assertEqual(stdout_manager1, stdout_manager2)
