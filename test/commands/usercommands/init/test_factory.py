from unittest import TestCase
from unittest.mock import Mock, patch

from guet.commands.usercommands.init.factory import InitCommandFactory


class TestInitFactory(TestCase):

    @patch('guet.commands.usercommands.init.factory.InitCommand')
    def test_returns_init_command(self, mock_InitCommand):
        factory = InitCommandFactory()
        command = factory.build([], Mock())
        self.assertEqual(mock_InitCommand.return_value, command)
