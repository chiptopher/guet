from e2e import DockerTest


class TestStart(DockerTest):

    def test_creates_hook_git_folder_in_current_path(self):
        self.guet_init()
        self.git_init()
        self.guet_start()
        self.execute()
        self.assert_file_exists('test-env/.git/hooks/commit-msg')

    def test_tells_user_that_a_git_folder_does_not_exist(self):
        self.guet_init()
        self.guet_start()
        self.execute()
        self.assert_text_in_logs(0, 'Git not initialized in this directory.')

    def test_tells_user_when_there_is_already_a_pre_commit_hook_and_gives_options_and_can_choose_to_cancel(self):
        self.guet_init()
        self.git_init()
        self.add_file('.git/hooks/pre-commit')
        self.guet_start(overwrite_answer='x')
        self.execute()
        self.assert_text_in_logs(1,
                                 'There is already commit hooks in this project. Would you like to overwrite (o), create (a) the file and put it in the hooks folder, or cancel (x)?')

    def test_passing_dash_a_to_command_creates_alongside_without_prompt(self):
        self.guet_init()
        self.git_init()
        self.add_file('.git/hooks/pre-commit')
        self.guet_start(args=['-a'])
        self.save_file_content('test-env/.git/hooks/pre-commit-guet')
        self.save_file_content('test-env/.git/hooks/post-commit-guet')
        self.save_file_content('test-env/.git/hooks/commit-msg-guet')
        self.execute()
        self.assertEqual('#! /usr/bin/env python3', self.get_file_text('test-env/.git/hooks/post-commit-guet')[0])
        self.assertEqual('#! /usr/bin/env python3', self.get_file_text('test-env/.git/hooks/commit-msg-guet')[0])
        self.assertEqual('#! /usr/bin/env python3', self.get_file_text('test-env/.git/hooks/pre-commit-guet')[0])

    def test_giving_a_to_create_alongside_creates_hooks_with_guet_appended_along_the_end(self):
        self.guet_init()
        self.git_init()
        self.add_file('.git/hooks/pre-commit')
        self.guet_start(overwrite_answer='a')
        self.save_file_content('test-env/.git/hooks/pre-commit-guet')
        self.save_file_content('test-env/.git/hooks/post-commit-guet')
        self.save_file_content('test-env/.git/hooks/commit-msg-guet')
        self.execute()
        self.assertEqual('#! /usr/bin/env python3', self.get_file_text('test-env/.git/hooks/post-commit-guet')[0])
        self.assertEqual('#! /usr/bin/env python3', self.get_file_text('test-env/.git/hooks/commit-msg-guet')[0])
        self.assertEqual('#! /usr/bin/env python3', self.get_file_text('test-env/.git/hooks/pre-commit-guet')[0])

    def test_uses_python3_shebang(self):
        self.git_init()
        self.guet_init()
        self.guet_start()
        self.guet_start()
        self.save_file_content('test-env/.git/hooks/pre-commit')
        self.save_file_content('test-env/.git/hooks/post-commit')
        self.execute()
        self.assertEqual('#! /usr/bin/env python3', self.get_file_text('test-env/.git/hooks/pre-commit')[0])
        self.assertEqual('#! /usr/bin/env python3', self.get_file_text('test-env/.git/hooks/post-commit')[0])
