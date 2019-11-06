
from e2e import DockerTest


class TestInit(DockerTest):

    def test_successful_init(self):
        self.guet_init()
        self.execute()
        self.assert_directory_exists('.guet')
        self.assert_file_exists('.guet/committernames')
        self.assert_file_exists('.guet/authornames')
        self.assert_file_exists('.guet/authoremails')
        self.assert_file_exists('.guet/committers')
        self.assert_file_exists('.guet/committersset')
        self.assert_file_exists('.guet/config')

    def test_multiple_calls_to_init_tells_user_config_folder_already_exists(self):
        self.guet_init()
        self.guet_init()
        self.execute()
        self.assert_text_in_logs(0, 'Config folder already exists.')
