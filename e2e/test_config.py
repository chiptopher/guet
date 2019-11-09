
from e2e import DockerTest


class TestConfig(DockerTest):

    def test_config_can_enable_or_disable_debug(self):
        self.guet_init()
        self.guet_config(['--debug=true'])
        self.save_file_content('.guet/config')

        self.execute()

        self.assertEqual('debug=True', self.get_file_text('.guet/config')[2])
