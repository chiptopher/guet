from e2e import DockerTest


class TestCommit(DockerTest):

    def test_adds_current_committers_to_commit_message(self):
        self.guet_init()
        self.guet_add('initials', 'name', 'email@localhost')
        self.guet_add('initials2', 'name2', 'email2@localhost')
        self.git_init()
        self.guet_start()
        self.guet_set(['initials', 'initials2'])
        self.add_file('A')
        self.git_add()
        self.git_commit('Initial commit')
        self.show_git_log()

        self.execute()

        self.assert_text_in_logs(11, 'Co-authored-by: name <email@localhost>')
        self.assert_text_in_logs(12, 'Co-authored-by: name2 <email2@localhost>')
