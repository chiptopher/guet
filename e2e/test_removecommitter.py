from e2e import DockerTest


class TestRemoveCommitter(DockerTest):

    def test_removes_committer_by_their_initials(self):
        self.guet_add('initials', 'name', 'email')
        self.guet_remove('initials')
        self.guet_get_committers()

        self.execute()

        self.assert_text_in_logs(0, 'All committers')
        self.assert_text_in_logs(1, '')

    def test_remove_ignores_case_of_initials(self):
        self.guet_add('initials', 'name', 'email')
        self.guet_remove('INITIALS')
        self.guet_get_committers()

        self.execute()

        self.assert_text_in_logs(0, 'All committers')
        self.assert_text_in_logs(1, '')

    def test_removing_initials_not_in_system_prints_error_message(self):
        self.guet_remove('initials')

        self.execute()

        self.assert_text_in_logs(0, "No committer exists with initials 'initials'")
