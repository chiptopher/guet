from e2e import DockerTest


class TestGet(DockerTest):
    def test_prints_help_message(self):
        self.guet_get_committers(include_help=True)
        self.execute()
        self.assert_text_in_logs(0, 'usage: guet get <identifier> [-flag, ...]')
        self.assert_text_in_logs(2, 'Get currently set information.')
        self.assert_text_in_logs(4, 'Valid Identifier')
        self.assert_text_in_logs(5, '\tcurrent - lists currently set committers')
        self.assert_text_in_logs(6, '\tall - lists all committers')

    def test_giving_no_args_prints_help_message(self):
        self.add_command('guet get')
        self.execute()
        self.assert_text_in_logs(0, 'usage: guet get <identifier> [-flag, ...]')
        self.assert_text_in_logs(2, 'Get currently set information.')
        self.assert_text_in_logs(4, 'Valid Identifier')
        self.assert_text_in_logs(5, '\tcurrent - lists currently set committers')
        self.assert_text_in_logs(6, '\tall - lists all committers')
