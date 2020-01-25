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

        self.assert_text_in_logs(10, '    Co-authored-by: name <email@localhost>')
        self.assert_text_in_logs(11, '    Co-authored-by: name2 <email2@localhost>')

    def test_replaces_co_authored_messages_when_editing_commit(self):
        self.guet_init()
        self.guet_add('initials', 'name', 'email@localhost')
        self.guet_add('initials2', 'name2', 'email2@localhost')
        self.guet_add('initials3', 'name3', 'email3@localhost')
        self.guet_add('initials4', 'name4', 'email4@localhost')
        self.git_init()
        self.guet_start()
        self.guet_set(['initials', 'initials2'])
        self.add_file('A')
        self.git_add()
        self.git_commit('Initial commit')
        self.guet_set(['initials3', 'initials4'])
        self.add_file('B')
        self.git_add()
        self.add_command('git commit --amend --no-edit')
        self.show_git_log()

        self.execute()
        self.assert_text_in_logs(16, '    Co-authored-by: name3 <email3@localhost>')
        self.assert_text_in_logs(17, '    Co-authored-by: name4 <email4@localhost>')

    def test_wont_allow_commit_if_guet_set_hasnt_been_done(self):
        self.guet_init()
        self.git_init()
        self.guet_start()
        self.add_file('A')
        self.git_add()
        self.git_commit('Initial commit')

        self.execute()

        self.assert_text_in_logs(1, 'You must set your pairs before you can commit.')

    def test_wont_allow_commits_in_guet_repo_if_pairs_havent_been_set_in_that_repo(self):
        self.guet_init()
        self.guet_add('initials', 'name', 'email@localhost')
        self.guet_add('initials2', 'name2', 'email2@localhost')
        self.guet_set(['initials', 'initials2'])
        self.add_command('mkdir test')
        self.change_directory('test')
        self.git_init()
        self.guet_start()
        self.add_file('A')
        self.git_add()
        self.git_commit('Initial commit')

        self.execute()

        self.assert_text_in_logs(1, 'You must set your pairs before you can commit.')

    def test_can_make_committs_in_multiple_repos_with_committers_set(self):
        self.guet_init()
        self.guet_add('initials', 'name', 'email@localhost')
        self.guet_add('initials2', 'name2', 'email2@localhost')
        self.guet_set(['initials', 'initials2'])
        self.add_command('mkdir test')
        self.change_directory('test')
        self.git_init()
        self.guet_start()
        self.guet_set(['initials', 'initials2'])
        self.add_file('A')
        self.git_add()
        self.git_commit('Initial commit')
        self.show_git_log()

        self.execute()

        self.assert_text_in_logs(10, '    Co-authored-by: name <email@localhost>')
        self.assert_text_in_logs(11, '    Co-authored-by: name2 <email2@localhost>')
