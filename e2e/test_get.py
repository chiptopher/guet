from e2e import DockerTest


class TestGet(DockerTest):
    def test_get_current_prints_currently_set_committers(self):
        self.guet_init()
        self.guet_add('initials1', 'name1', 'email1')
        self.guet_add('initials2', 'name2', 'email2')
        self.guet_set(['initials1', 'initials2'])
        self.guet_get_current()
        self.save_file_content('.guet/errors')

        self.execute()

        self.assert_text_in_logs(0, 'Currently set committers')
        self.assert_text_in_logs(1, 'initials1 - name1 <email1>')
        self.assert_text_in_logs(2, 'initials2 - name2 <email2>')

    def test_get_committers_prints_all_committers_on_the_system(self):
        self.guet_init()
        self.guet_add('initials1', 'name1', 'email1')
        self.guet_add('initials2', 'name2', 'email2')
        self.guet_set(['initials1', 'initials2'])
        self.guet_get_committers()
        self.save_file_content('.guet/errors')

        self.execute()

        self.assert_text_in_logs(0, 'All committers')
        self.assert_text_in_logs(1, 'initials1 - name1 <email1>')
        self.assert_text_in_logs(2, 'initials2 - name2 <email2>')
