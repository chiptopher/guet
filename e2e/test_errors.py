from e2e import DockerTest


class TestError(DockerTest):

    def test_uncaught_errors_are_written_to_log_file(self):
        self.guet_init()
        self.add_command('guet notacommand')
        self.save_file_content('.guet/errors')

        self.execute()

        self.assertEqual(self.get_file_text('.guet/errors')[0], 'Traceback (most recent call last):')
