# pylint: disable=line-too-long

import time

from e2e import DockerTest


class TestGuetSet(DockerTest):
    def test_set_gracefully_displays_error_message_when_setting_committer_with_unknown_initials(self):
        self.git_init()
        self.guet_init()
        self.guet_set(['ui'])

        self.execute()

        self.assert_text_in_logs(2, "No committer exists with initials 'ui'")

    def test_adds_committer_initials_and_current_millis_to_committersset_file(self):
        start_time = int(round(time.time() * 1000))
        self.git_init()
        self.guet_init()
        self.guet_add('initials1', 'name1', 'email1')
        self.guet_add('initials2', 'name2', 'email2')
        self.guet_set(['initials1', 'initials2'])
        self.save_file_content('.guet/committersset')
        self.save_file_content('.guet/committers')

        self.execute()

        committers_set = self.get_file_text('.guet/committersset')

        set_text = committers_set[0]
        set_text_split = set_text.split(',')
        self.assertEqual('initials1', set_text_split[0])
        self.assertEqual('initials2', set_text_split[1])
        self.assertTrue(start_time + 10000 >
                        int(set_text_split[2]) > start_time)

    def test_set_committers_ignores_case_of_initials(self):
        self.git_init()
        self.guet_init()
        self.guet_add('initials1', 'name1', 'email1')
        self.guet_add('initials2', 'name2', 'email2')
        self.guet_set(['INITIALS1', 'initials2'])
        self.guet_get_current()

        self.execute()

        self.assert_text_in_logs(5, 'Current committers')
        self.assert_text_in_logs(6, 'initials1 - name1 <email1>')
        self.assert_text_in_logs(7, 'initials2 - name2 <email2>')

    def test_set_committers_displays_help_message_when_no_initials_given(self):
        self.guet_set([])
        self.execute()
        self.assert_text_in_logs(
            0, 'usage: guet set <initials> [<initials> ...]')

    def test_errors_if_guet_set_ran_in_folder_with_no_git(self):
        self.guet_add('initials1', 'name1', 'email1')
        self.guet_add('initials2', 'name2', 'email2')
        self.guet_set(['initials1', 'initials2'])

        self.execute()

        self.assert_text_in_logs(0, 'Git not installed in this directory.')

    def test_can_set_committers_from_subfolder(self):
        self.git_init()
        self.guet_add('initials1', 'name1', 'email1')
        self.guet_add('initials2', 'name2', 'email2')
        self.guet_init()
        self.add_command('mkdir api')
        self.change_directory('api')
        self.guet_set(['initials1', 'initials2'])

        self.save_file_content('.guet/committersset')
        self.save_file_content('.guet/committers')

        self.execute()

        committers_set = self.get_file_text('.guet/committersset')
        set_text = committers_set[0]
        set_text_split = set_text.split(',')
        self.assertEqual('initials1', set_text_split[0])
        self.assertEqual('initials2', set_text_split[1])

    def test_setting_committers_includes_local_committers(self):
        self.git_init()
        self.guet_init()
        self.guet_add('initials1', 'name1', 'email1', local=True)
        self.guet_add('initials2', 'name2', 'email2')
        self.add_command('mkdir api')
        self.change_directory('api')
        self.guet_set(['initials1', 'initials2'])
        self.guet_get_current()
        self.save_file_content('test-env/.guet/committers')

        self.execute()

        self.assert_text_in_logs(5, 'Current committers')
        self.assert_text_in_logs(6, 'initials1 - name1 <email1>')
        self.assert_text_in_logs(7, 'initials2 - name2 <email2>')
