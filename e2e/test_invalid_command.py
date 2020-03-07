from e2e import DockerTest


class TestInvalidCommand(DockerTest):
    def test_shows_usage_when_bad_command_given(self):
        self.add_command('guet invalid')
        self.execute()
        self.assert_text_in_logs(0, 'guet has no command "invalid" that can be ran.')
        self.assert_text_in_logs(2, 'usage: guet <command>')
