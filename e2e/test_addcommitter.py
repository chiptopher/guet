
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
        self.execute()
        self.assert_text_in_logs(0, 'Not enough arguments.')

    def test_add_commiter_requires_that_you_guet_init_first(self):
        self.guet_add('initials', 'name', 'email')
        self.execute()
        self.assert_text_in_logs(0,
                                 'guet has not been initialized yet! Please do so by running the command "guet init".')
