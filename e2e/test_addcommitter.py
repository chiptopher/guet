from e2e import DockerTest


class TestAddUser(DockerTest):

    def test_add_committer_too_many_arguments_prints_error_message(self):
        self.guet_init()
        self.add_command('guet add initials name email extra')
        self.execute()
        self.assert_text_in_logs(0, 'Too many arguments.')

    def test_add_committer_not_enough_args_prints_the_error_message_and_help_for_command(self):
        self.guet_init()
        self.add_command('guet add initials name')
        self.save_file_content('.guet/errors')
        self.execute()
        self.assert_text_in_logs(0, 'Not enough arguments.')

    def test_add_commiter_requires_that_you_guet_init_first(self):
        self.guet_add('initials', 'name', 'email')
        self.execute()
        self.assert_text_in_logs(0,
                                 'guet has not been initialized yet! Please do so by running the command "guet init".')

    def test_adds_committer_to_committers_file(self):
        self.guet_init()
        self.guet_add('initials', 'name', 'email')
        self.save_file_content('.guet/committers')

        self.execute()

        committers_file = self.get_file_text('.guet/committers')
        self.assertEqual('initials,name,email', committers_file[0])

    def test_prompts_user_to_overwrite_committers_when_given_same_initials(self):
        self.guet_init()
        self.guet_add('initials', 'name1', 'email1')
        self.guet_add('initials', 'name2', 'email2', overwrite_answer='y')
        self.guet_get_committers()
        self.guet_add('initials', 'name1', 'email1', overwrite_answer='x')
        self.guet_get_committers()
        self.execute()
        self.assert_text_in_logs(0, ('Matching initials "initials". Adding "name2" <email2> '
                                     'will overwrite "name1" <email1>. Would you '
                                     'like to continue (y) or cancel (x)?'))
        self.assert_text_in_logs(2, 'initials - name2 <email2>')
        self.assert_text_in_logs(5, 'initials - name2 <email2>')

    def test_initials_are_lower_case_when_saved(self):
        self.guet_init()
        self.guet_add('INITIALS', 'name1', 'email1')
        self.guet_get_committers()
        self.execute()
        self.assert_text_in_logs(1, 'initials - name1 <email1>')

    def test_including_local_flag_adds_committer_to_the_repository(self):
        self.guet_init()
        self.git_init()
        self.guet_add('initials', 'name1', 'email1', local=True)
        self.save_file_content('test-env/.guet/committers')

        self.execute()

        text = self.get_file_text('test-env/.guet/committers')
        self.assertListEqual(['initials,name1,email1'], text)

    def test_adding_local_committers_only_saves_the_local_committers(self):
        self.guet_init()
        self.git_init()
        self.guet_add('initials1', 'name1', 'email1')
        self.guet_add('initials2', 'name2', 'email2', local=True)
        self.save_file_content('test-env/.guet/committers')

        self.execute()

        text = self.get_file_text('test-env/.guet/committers')
        self.assertListEqual(['initials2,name2,email2'], text)

    def test_prints_error_message_when_adding_local_committer_that_has_same_initials_as_global_committer(self):
        self.guet_init()
        self.guet_add('initials', 'name1', 'email1')
        self.guet_add('initials', 'name2', 'emial2', local=True)

        self.execute()

        self.assert_text_in_logs(0, ('Adding committer with initials "initials" shadows the '
                                     'global committer "initials" - "name1" <email1>'))

    def test_adding_local_committer_in_subfolder_adds_committer_to_root_directory(self):
        self.guet_init()
        self.git_init()
        self.add_command('mkdir ui')
        self.change_directory('ui')
        self.guet_add('initials1', 'name1', 'email1', local=True)
        self.save_file_content('test-env/.guet/committers')

        self.execute()

        text = self.get_file_text('test-env/.guet/committers')
        self.assertListEqual(['initials1,name1,email1'], text)

    def test_adding_local_committers_with_no_git_prints_error_message(self):
        self.guet_init()
        self.guet_add('initials1', 'name1', 'email1', local=True)

        self.execute()

        self.assert_text_in_logs(0, 'No git folder, so project root cannot be determined.')
