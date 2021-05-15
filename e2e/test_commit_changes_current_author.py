from e2e import DockerTest


class TestGuetCommitRotatesAuthor(DockerTest):

    def test_committers_are_swapped_as_author_every_commit(self):
        self.guet_add('initials', 'name', 'email@localhost')
        self.guet_add('initials2', 'name2', 'email2@localhost')
        self.guet_add('initials3', 'name3', 'email3@localhost')
        self.git_init()
        self.guet_init()
        self.guet_set(['initials', 'initials2', 'initials3'])
        self.add_file('A')
        self.git_add()
        self.git_commit('Initial commit')
        self.add_file('B')
        self.git_add()
        self.git_commit('Second commit')
        self.add_file('C')
        self.git_add()
        self.git_commit('Third commit')
        self.show_git_log()

        self.execute()

        self.assert_text_in_logs(36, 'Author: {} <{}>'.format('name', 'email@localhost'))
        self.assert_text_in_logs(26, 'Author: {} <{}>'.format('name2', 'email2@localhost'))
        self.assert_text_in_logs(16, 'Author: {} <{}>'.format('name3', 'email3@localhost'))

    def test_second_commit_uses_second_pair_name_and_email(self):
        self.guet_add('initials', 'name', 'email@localhost')
        self.guet_add('initials2', 'name2', 'email2@localhost')
        self.git_init()
        self.guet_init()
        self.guet_set(['initials', 'initials2'])
        self.add_file('A')
        self.git_add()
        self.git_commit('initial commit')
        self.add_file('B')
        self.git_add()
        self.git_commit('second commit')
        self.show_git_log()

        self.execute()

        self.assert_text_in_logs(12, 'Author: {} <{}>'.format('name2', 'email2@localhost'))
