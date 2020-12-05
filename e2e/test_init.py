from e2e import DockerTest


class TestInit(DockerTest):

    def test_successful_init(self):
        self.guet_init()
        self.save_file_content('.guet/config')

        self.execute()

        self.assert_directory_exists('.guet')
        self.assert_file_exists('.guet/committernames')
        self.assert_file_exists('.guet/committers')
        self.assert_file_exists('.guet/committersset')
        self.assert_file_exists('.guet/config')

        self.assertEqual('', self.get_file_text('.guet/config')[1])
