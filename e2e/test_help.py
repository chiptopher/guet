from e2e import DockerTest


class TestInit(DockerTest):
    def test_guet_command_by_itself_displays_help_message(self):
        self.add_command('guet')

        self.execute()

        self.assert_text_in_logs(0, 'usage: guet <command>')

