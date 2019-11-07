
from e2e import DockerTest


class TestConfig(DockerTest):

    def test_config_can_enable_or_disable_the_force_resetting_of_pairs(self):
        self.guet_init()
        self.guet_config(['--pairReset=false'])
        self.save_file_content('.guet/config')

        self.execute()

        self.assertEqual('pairReset=False', self.get_file_text('.guet/config')[0])
