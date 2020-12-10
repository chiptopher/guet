from e2e import DockerTest


class TestAddUser(DockerTest):

    def test_adds_committer_to_committers_file(self):
        self.guet_init()
        self.guet_add('initials', 'name', 'email')
        self.save_file_content('.guet/committers')

        self.execute()

        committers_file = self.get_file_text('.guet/committers')
        self.assertEqual('initials,name,email', committers_file[0])

    def test_add_committer_not_enough_args_prints_the_error_message_and_help_for_command(self):
        self.add_command('guet add initials name')
        self.save_file_content('.guet/errors')
        self.execute()
        self.assert_text_in_logs(0, 'Not enough arguments.')

    def test_add_committer_too_many_arguments_prints_error_message(self):
        self.add_command('guet add initials name email extra')
        self.execute()
        self.assert_text_in_logs(0, 'Too many arguments.')

    def test_prompts_user_to_overwrite_committers_when_given_same_initials(self):
        self.guet_add('initials', 'name1', 'email1')
        self.guet_add('initials', 'name2', 'email2', overwrite_answer='y')
        self.guet_get_committers()
        self.guet_add('initials', 'name1', 'email1', overwrite_answer='x')
        self.guet_get_committers()
        self.execute()
        self.assert_text_in_logs(0, ('Matching initials "initials". Adding "name2" <email2> '
                                     'will overwrite "name1" <email1>. Would you '
                                     'like to continue(y) or cancel(x)?'))
        self.assert_text_in_logs(2, 'initials - name2 <email2>')
        self.assert_text_in_logs(6, 'initials - name2 <email2>')

