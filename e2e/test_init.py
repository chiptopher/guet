# pylint: disable=line-too-long

from e2e import DockerTest
from guet.steps.check.git_required_check import GIT_REQUIRED_MESSAGE


class TestInit(DockerTest):

    def test_successful_init(self):
        self.git_init()
        self.guet_init()
        self.save_file_content('.guet/config')

        self.execute()

        self.assert_directory_exists('.guet')
        self.assert_file_exists('.guet/committernames')
        self.assert_file_exists('.guet/committers')
        self.assert_file_exists('.guet/committersset')
        self.assert_file_exists('.guet/config')

        self.assertEqual('', self.get_file_text('.guet/config')[1])

    def test_tells_user_when_guet_has_successfully_started(self):
        self.git_init()
        self.guet_init()
        self.execute()
        self.assert_text_in_logs(
            1, 'guet successfully started in this repository.')

    def test_creates_hook_git_folder_in_current_path(self):
        self.git_init()
        self.guet_init()
        self.execute()
        self.assert_file_exists('test-env/.git/hooks/commit-msg')

    def test_tells_user_that_a_git_folder_does_not_exist(self):
        self.guet_init()
        self.execute()
        self.assert_text_in_logs(0, GIT_REQUIRED_MESSAGE)

    def test_tells_user_when_there_is_already_a_pre_commit_hook_and_gives_options_and_can_choose_to_cancel(self):
        self.git_init()
        self.add_file('.git/hooks/pre-commit')
        self.guet_init(overwrite_answer='x')
        self.execute()
        self.assert_text_in_logs(1,
                                 'There is already commit hooks in this project. You can')
        self.assert_text_in_logs(2, '  (o) overwrite current hooks. This will delete any matching hooks.')
        self.assert_text_in_logs(3, ('  (a) create guet hooks alongside current ones.'
                                     'This will create them with \'-guet\' appended on the name of the hook file.'))
        self.assert_text_in_logs(4, '  (x) cancel the request. This will do nothing.')

    def test_passing_dash_a_to_command_creates_alongside_without_prompt(self):
        self.git_init()
        self.add_file('.git/hooks/pre-commit')
        self.guet_init(args=['-a'])
        self.save_file_content('test-env/.git/hooks/pre-commit-guet')
        self.save_file_content('test-env/.git/hooks/post-commit-guet')
        self.save_file_content('test-env/.git/hooks/commit-msg-guet')
        self.execute()
        self.assertEqual('#! /usr/bin/env python3', self.get_file_text('test-env/.git/hooks/post-commit-guet')[0])
        self.assertEqual('#! /usr/bin/env python3', self.get_file_text('test-env/.git/hooks/commit-msg-guet')[0])
        self.assertEqual('#! /usr/bin/env python3', self.get_file_text('test-env/.git/hooks/pre-commit-guet')[0])

    def test_giving_a_to_create_alongside_creates_hooks_with_guet_appended_along_the_end(self):
        self.git_init()
        self.add_file('.git/hooks/pre-commit')
        self.guet_init(overwrite_answer='a')
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
        self.save_file_content('test-env/.git/hooks/pre-commit')
        self.save_file_content('test-env/.git/hooks/post-commit')
        self.execute()
        self.assertEqual('#! /usr/bin/env python3', self.get_file_text('test-env/.git/hooks/pre-commit')[0])
        self.assertEqual('#! /usr/bin/env python3', self.get_file_text('test-env/.git/hooks/post-commit')[0])

    def test_giving_dash_o_flag_overwrites_current_hooks_without_prompt(self):
        self.git_init()
        self.add_file('.git/hooks/pre-commit')
        self.guet_init(args=['-o'])
        self.save_file_content('test-env/.git/hooks/pre-commit')
        self.save_file_content('test-env/.git/hooks/post-commit')
        self.save_file_content('test-env/.git/hooks/commit-msg')
        self.execute()
        self.assertEqual('#! /usr/bin/env python3', self.get_file_text('test-env/.git/hooks/post-commit')[0])
        self.assertEqual('#! /usr/bin/env python3', self.get_file_text('test-env/.git/hooks/commit-msg')[0])
        self.assertEqual('#! /usr/bin/env python3', self.get_file_text('test-env/.git/hooks/pre-commit')[0])

    def test_attempting_to_start_in_project_without_hooks_creates_hooks_folder(self):
        self.git_init()
        self.add_command('rm -rf .git/hooks')
        self.guet_init()
        self.execute()

        self.assert_text_in_logs(1, 'No hooks directory found, creating one.')

    def test_tells_guet_not_started_if_x_is_pressed(self):
        self.git_init()
        self.add_file('.git/hooks/pre-commit')
        self.guet_init(overwrite_answer='x')
        self.execute()
        self.assert_text_in_logs(5, 'guet not started.')
        self.assert_text_not_in_logs(6, 'guet successfully started in this repository.')

    def test_can_set_location_for_guet_hooks(self):
        self.git_init()
        self.add_command('mkdir .other')
        self.guet_init(args=['--location', '.other'])
        self.execute()
        self.assert_file_exists('test-env/.other/pre-commit')
        self.assert_file_exists('test-env/.other/post-commit')
        self.assert_file_exists('test-env/.other/commit-msg')
