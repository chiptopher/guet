from e2e import DockerTest


class TestHelp(DockerTest):
    def test_guet_command_by_itself_displays_help_message(self):
        self.add_command('guet')

        self.execute()

        self.assert_text_in_logs(0, 'usage: guet <command>')

    def test_guet_command_shows_help_message_when_dash_h_is_given(self):
        self.add_command('guet -h')

        self.execute()

        self.assert_text_in_logs(0, 'usage: guet <command>')

    def test_guet_command_shows_help_message_when_dash_dash_help_is_given(self):
        self.add_command('guet --help')

        self.execute()

        self.assert_text_in_logs(0, 'usage: guet <command>')
