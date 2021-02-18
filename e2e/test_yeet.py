from e2e import DockerTest


class TestYeet(DockerTest):

    def test_yeets_guet_from_repository(self):
        self.git_init()
        self.guet_init()
        self.guet_add('initials', 'name', 'email', local=True)
        self.guet_yeet()
        self.execute()
        self.assert_text_in_logs(2, 'guet tracking removed from this repository')


    def test_commit_doesnt_have_co_authored_because_hooks_removed(self):
        self.git_init()
        self.guet_init()
        self.guet_add('initials', 'name', 'email@localhost')
        self.guet_add('initials2', 'name2', 'email2@localhost')
        self.guet_set(['initials', 'initials2'])
        self.add_file('A')
        self.guet_yeet()
        self.git_add()
        self.git_commit('Initial commit')
        self.show_git_log()

        self.execute()

        self.assert_text_in_logs(12, '')
        self.assert_text_in_logs(13, '    Initial commit')
        self.assert_text_in_logs(14, '')

    def test_yeet_doesnt_remove_non_guet_hooks(self):
        self.git_init()
        self.add_file('.git/hooks/commit-msg')
        self.guet_init(overwrite_answer='a')
        self.guet_yeet()
        self.save_file_content('test-env/.git/hooks/commit-msg')
        self.execute()
        self.assert_file_exists('test-env/.git/hooks/commit-msg')
