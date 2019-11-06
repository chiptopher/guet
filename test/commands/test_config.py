import unittest

from guet.commands.config import ConfigSetCommand


class ConfigSetTest(unittest.TestCase):

    def test_help_message(self):
        command = ConfigSetCommand([])
        self.assertEqual(ConfigSetCommand.HELP_MESSAGE, command.help())

    def test_short_help_message(self):
        command = ConfigSetCommand([])
        self.assertEqual(ConfigSetCommand.SHORT_HELP_MESSAGE, command.get_short_help_message())
