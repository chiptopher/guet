import time
import unittest
from typing import Dict, List

import docker

from e2e.dockertest.file_system import process_file_system, DockerFile
from e2e.dockertest.logs import process_logs


def _not_called_execute(f):
    def wrapper(*args, **kwargs):
        if not args[0].execute_called:
            args[0].fail('You must call execute before making assertions.')
        return f(*args, **kwargs)

    return wrapper


def _called_execute(f):
    def wrapper(*args, **kwargs):
        if args[0].execute_called:
            args[0].fail('You cannot change the run parameters after execute already called.')
        return f(*args, **kwargs)

    return wrapper


class DockerTest(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        docker_client = docker.from_env()
        # project_root_directory = abspath(join(abspath(__file__), '../../..'))
        # docker_client.images.build(path=project_root_directory, tag='guettest:0.1.0')
        docker_client.close()

    def __init__(self, *args, **kwargs):
        super(DockerTest, self).__init__(*args, **kwargs)
        self.logs = None
        self.file_system = None

        self.execute_called = False
        self.commands = []
        self.files_to_save = []

    def execute(self):
        docker_client = docker.from_env()
        container = docker_client.containers.run('guettest:0.1.0',
                                                 self._generate_commands_string_to_pass_to_run(),
                                                 detach=True)
        time.sleep(1)

        self.file_system = process_file_system(container)
        self.logs = process_logs(container, self.file_system)

        docker_client.close()
        self.execute_called = True

    @_called_execute
    def guet_init(self, arguments: List[str] = None):
        command = 'guet init'
        if arguments:
            command = command + ' ' + ' '.join(arguments)
        self.commands.append(command)

    @_called_execute
    def guet_add(self, initials: str, name: str, email: str):
        command = f'guet add {initials} "{name}" {email}'
        self.commands.append(command)

    @_called_execute
    def add_command(self, command: str):
        self.commands.append(command)

    @_called_execute
    def guet_start(self, overwrite_answer: str = None):
        command = 'guet start'
        if overwrite_answer:
            command = f'printf {overwrite_answer} | {command}'
        self.commands.append(command)

    @_called_execute
    def git_init(self):
        self.commands.append('git init')

    @_called_execute
    def save_file_content(self, file_path: str):
        self.commands.append(f'echo start cat for {file_path}')
        self.commands.append(f'cat /root/test-env/{file_path}')
        self.commands.append(f'echo end cat for {file_path}')

    @_called_execute
    def add_file(self, file_path: str, text: str = None):
        command = f'touch {file_path}'
        if text:
            command = f'echo "{text}" >> {file_path}'
        self.commands.append(command)

    @_not_called_execute
    def get_file_text(self, file_path: str) -> List[str]:
        file = self.file_system.get_file_from_test_env(file_path)
        return file.lines

    @_not_called_execute
    def assert_directory_exists(self, path: str):
        self._file_or_directory_exists_in_file_system(path)

    @_not_called_execute
    def assert_text_in_logs(self, position_in_logs: int, expected_text: str):
        self.assertEqual(expected_text, self.logs[position_in_logs])

    @_not_called_execute
    def assert_file_exists(self, expected_path):
        self._file_or_directory_exists_in_file_system(expected_path)

    def _generate_commands_string_to_pass_to_run(self) -> str:
        return f'/bin/sh -c "{"; ".join(self.commands)}"'

    def _file_or_directory_exists_in_file_system(self, path: str):
        self.assertTrue(self.file_system.get_file_from_root(path) is not None)

