import guet
from e2e import DockerTest


class TestAddUser(DockerTest):

    def test_prints_version(self):
        self.add_command('guet --version')
        self.execute()
        self.assert_text_in_logs(0, guet.__version__)
