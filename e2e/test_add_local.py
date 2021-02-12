# pylint: disable=line-too-long

from e2e import DockerTest


class TestAddUser(DockerTest):

    def test_including_local_flag_adds_committer_to_the_repository(self):
        self.git_init()
        self.guet_init()
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

    def test_prints_warning_message_when_adding_local_committer_that_has_same_initials_as_global_committer(self):
        self.git_init()
        self.guet_init()
        self.guet_add('initials', 'name1', 'email1')
        self.guet_add('initials', 'name2', 'email2', local=True)
        self.save_file_content('test-env/.guet/committers')

        self.execute()

        self.assert_text_in_logs(
            2, ('Adding committer with initials "initials" will overshadow global committer with same initials.'))
        text = self.get_file_text('test-env/.guet/committers')
        self.assertListEqual(['initials,name2,email2'], text)

    def test_adding_local_committer_in_subfolder_adds_committer_to_root_directory(self):
        self.git_init()
        self.guet_init()
        self.add_command('mkdir ui')
        self.change_directory('ui')
        self.guet_add('initials1', 'name1', 'email1', local=True)
        self.save_file_content('test-env/.guet/committers')

        self.execute()

        text = self.get_file_text('test-env/.guet/committers')
        self.assertListEqual(['initials1,name1,email1'], text)

    def test_add_local_requires_git_initialized_before_committing(self):
        self.guet_add('initials1', 'name1', 'email1', local=True)

        self.execute()
        self.assert_text_in_logs(0, ("Git not installed in this directory."))
