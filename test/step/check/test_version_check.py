import unittest
from guet.steps.check.version_check import VersionCheck


class TestVersionCheck(unittest.TestCase):
    def test_should_stop_if_version_flag_in_args(self):
        check = VersionCheck()
        self.assertTrue(check.should_stop(['--version']))
        self.assertTrue(check.should_stop(['-v']))
        self.assertFalse(check.should_stop(['anything', 'else']))
