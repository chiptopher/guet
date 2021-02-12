from e2e import DockerTest


class TestYeet(DockerTest):

    def test_yeets_guet_from_repository(self):
        self.git_init()
        self.guet_init()
        self.guet_add('initials', 'name', 'email', local=True)
        self.guet_yeet()
        self.execute()
        self.assert_text_in_logs(2, 'guet tracking removed from this repository')
