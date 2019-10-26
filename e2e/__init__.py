import time
import unittest
from typing import List

import docker
from os.path import abspath, join


def _execute_called(f):
    def wrapper(*args):
        if not args[0].execute_called:
            args[0].fail('You must call execute before making assertions.')
        return f(*args)

    return wrapper


class DockerTest(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        docker_client = docker.from_env()
        project_root_directory = abspath(join(abspath(__file__), '../..'))
        docker_client.images.build(path=project_root_directory, tag='guettest:0.1.0')
        docker_client.close()

    def __init__(self, *args, **kwargs):
        super(DockerTest, self).__init__(*args, **kwargs)
        self.logs = None
        self.file_system = None

        self.execute_called = False
        self.commands = []

    def execute(self):
        docker_client = docker.from_env()
        container = docker_client.containers.run('guettest:0.1.0', self._generate_commands_string_to_pass_to_run(),
                                                 detach=True)
        time.sleep(1)
        actual_logs = container.logs()
        encoded = actual_logs.decode('utf-8')
        split = encoded.split('\n')
        self.logs = split
        self.file_system = container.diff()
        docker_client.close()
        self.execute_called = True

    def guet_init(self, arguments: List[str] = None):
        command = 'guet init'
        if arguments:
            command = command + ' ' + ' '.join(arguments)
        self.commands.append(command)

    @_execute_called
    def assert_directory_exists(self, path: str):
        self._file_or_directory_exists_in_file_system(path)

    @_execute_called
    def assert_text_in_logs(self, position_in_logs: int, expected_text: str):
        self.assertEqual(expected_text, self.logs[position_in_logs])

    @_execute_called
    def assert_file_exists(self, expected_path):
        self._file_or_directory_exists_in_file_system(expected_path)

    def _generate_commands_string_to_pass_to_run(self) -> str:
        return f'/bin/sh -c "{"; ".join(self.commands)}"'

    def _file_or_directory_exists_in_file_system(self, path: str):
        found = False
        for file in self.file_system:
            if file['Path'] == f'/root/{path}':
                found = True
        self.assertTrue(found)
