from e2e import DockerTest


class TestGuetCommitRotatesAuthor(DockerTest):

    def test_commits_swaps_pairs_once(self):
        self.guet_init()
        self.guet_add('initials', 'name', 'email@localhost')
        self.guet_add('initials2', 'name2', 'email2@localhost')
        self.git_init()
        self.guet_start()
        self.guet_set(['initials', 'initials2'])
        self.add_file('A')
        self.git_add()
        self.git_commit('Initial commit')
        self.save_file_content('.guet/authornames')
        self.save_file_content('.guet/authoremails')

        self.execute()

        self.assertEqual('name2', self.get_file_text('.guet/authornames')[0])
        self.assertEqual('email2@localhost', self.get_file_text('.guet/authoremails')[0])

    def test_mob_participants_can_swap_multiple_times(self):
        self.guet_init()
        self.guet_add('initials', 'name', 'email@localhost')
        self.guet_add('initials2', 'name2', 'email2@localhost')
        self.guet_add('initials3', 'name3', 'email3@localhost')
        self.git_init()
        self.guet_start()
        self.guet_set(['initials', 'initials2', 'initials3'])
        self.add_file('A')
        self.git_add()
        self.git_commit('Initial commit')
        self.add_file('B')
        self.git_add()
        self.git_commit('Second commit')
        self.save_file_content('.guet/authornames')
        self.save_file_content('.guet/authoremails')
        self.save_file_content('.guet/committers')
        self.save_file_content('.guet/committersset')

        self.execute()

        self.assertEqual('name3', self.get_file_text('.guet/authornames')[0])
        self.assertEqual('email3@localhost', self.get_file_text('.guet/authoremails')[0])

    def test_second_commit_uses_second_pair_name_and_email(self):
        self.guet_init()
        self.guet_add('initials', 'name', 'email@localhost')
        self.guet_add('initials2', 'name2', 'email2@localhost')
        self.git_init()
        self.guet_set(['initials', 'initials2'])
        self.guet_start()
        self.add_file('A')
        self.git_add()
        self.git_commit('initial commit')
        self.add_file('B')
        self.git_add()
        self.git_commit('second commit')
        self.show_git_log()

        self.execute()

        self.assert_text_in_logs(8, 'Author: {} <{}>'.format('name2', 'email2@localhost'))

