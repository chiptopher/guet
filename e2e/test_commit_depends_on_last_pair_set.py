

from e2e import DockerTest


class TestGuetCommitRotatesAuthor(DockerTest):

    def test_commits_swaps_pairs_once(self):
        self.guet_init()
        self.guet_add('initials', 'name', 'email@localhost')
        self.guet_add('initials2', 'name2', 'email2@localhost')
        self.git_init()
        self.guet_start()
        self.add_command(f"faketime '2008-12-24 08:15:42' guet set initials initials2")
        self.add_file('A')
        self.git_add()
        # TODO make it so that you don't need to do a global configuration for committing to work
        self.add_command('git config --global user.name test')
        self.add_command('git config --global user.email test')
        self.git_commit('initial commit')

        self.execute()

        self.assert_text_in_logs(2, 'You have not reset pairs in over twenty four hours!')
        self.assert_text_in_logs(3, "Please reset your pairs by using guet set and including your pairs' initials")
