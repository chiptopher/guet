from e2e import DockerTest


class TestAddUser(DockerTest):

    def test_adds_committer_to_committers_file(self):
        self.guet_init()
        self.guet_add('initials', 'name', 'email')
        self.save_file_content('.guet/committers')

        self.execute()

        committers_file = self.get_file_text('.guet/committers')
        self.assertEqual('initials,name,email', committers_file[0])
