
from e2e import DockerTest
from guet.commands.init_required_decorator import INIT_REQUIRED_ERROR_MESSAGE


class TestConfig(DockerTest):

    def test_config_can_enable_or_disable_debug(self):
        self.guet_init()
        self.guet_config(['--debug=true'])
        self.save_file_content('.guet/config')

        self.execute()

        self.assertEqual('debug=True', self.get_file_text('.guet/config')[2])

    def test_config_requires_init_to_run(self):
        self.guet_config(['--debug=True'])
        self.execute()
        self.assert_text_in_logs(0, INIT_REQUIRED_ERROR_MESSAGE)
