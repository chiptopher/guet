#pylint: disable=too-many-public-methods

import time
import unittest
from os.path import abspath, join
from typing import List

import docker  # pylint: disable=import-error

from e2e.dockertest.file_system import FileSystem, process_file_system
from e2e.dockertest.logs import process_logs


def _not_called_execute(func):
    def wrapper(*args, **kwargs):
        if not args[0].execute_called:
            args[0].fail('You must call execute before making assertions.')
        return func(*args, **kwargs)

    return wrapper


def _called_execute(func):
    def wrapper(*args, **kwargs):
        if args[0].execute_called:
            args[0].fail(
                'You cannot change the run parameters after execute already called.')
        return func(*args, **kwargs)

    return wrapper


def _print_logs_when_test_fails(func):
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except AssertionError as exception:
            print('========= Start Message log =========')
            for count, value in enumerate(args[0].logs):
                print(f'{count}\t: {value}')
            print('=========  End Message log  =========')
            raise exception

    return wrapper


class DockerTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        docker_client = docker.from_env()
        project_root_directory = abspath(join(abspath(__file__), '../../..'))
        docker_client.images.build(
            path=project_root_directory, tag='guettest:0.1.0')
        docker_client.close()

    def __init__(self, *args, **kwargs):
        super(DockerTest, self).__init__(*args, **kwargs)
        self.logs = None
        self.file_system: FileSystem = None
        self.execute_command = None

        self.execute_called = False
        self.commands = []
        self.files_to_save = []
        self.init_called = False

    def execute(self):
        if self.init_called:
            self.save_file_content('.guet/config')
        docker_client = docker.from_env()
        self.execute_command = self._generate_commands_string_to_pass_to_run()
        container = docker_client.containers.run('guettest:0.1.0',
                                                 self.execute_command,
                                                 detach=True)
        time.sleep(1)

        self.file_system = process_file_system(container)
        self.logs = process_logs(container, self.file_system)

        docker_client.close()
        self.execute_called = True

    def change_directory(self, path: str):
        self.add_command(f'cd {path}')

    def return_to_default_directory(self):
        self.add_command('cd ~/test-env')

    @_called_execute
    def guet_config(self, flags: List[str] = list()): # pylint: disable=dangerous-default-value
        command = f'guet config {" ".join(flags)}'
        self.add_command(command)

    @_called_execute
    def guet_add(self, initials: str, name: str, email: str, *, overwrite_answer=None, local=False):
        command = f'guet add {initials} "{name}" {email}'
        if overwrite_answer:
            command = f'printf {overwrite_answer} | {command}'
        if local:
            command = f'guet add --local {initials} "{name}" {email}'
        self.add_command(command)

    @_called_execute
    def guet_remove(self, initials: str):
        self.add_command(f'guet remove {initials}')

    @_called_execute
    def guet_get_committers(self, include_help=False):
        command = f'guet get all'
        if include_help:
            command += ' --help'
        self.add_command(command)

    @_called_execute
    def guet_get_current(self):
        self.add_command(f'guet get current')

    @_called_execute
    def add_command(self, command: str):
        self.commands.append(command)

    @_called_execute
    def guet_init(self, overwrite_answer: str = None, args: List[str] = []): # pylint: disable=dangerous-default-value
        command = 'guet init'
        command = f'{command} {" ".join(args)}'
        if overwrite_answer:
            command = f'printf {overwrite_answer} | {command}'
        self.add_command(command)

    def guet_set(self, initials: List[str]):
        self.add_command(f'guet set {" ".join(initials)}')

    def guet_yeet(self):
        self.add_command('guet yeet')

    @_called_execute
    def git_init(self, _: str = None, *, with_author_config: bool = False):
        self.add_command('git init')
        if with_author_config:
            self.add_command('git config --global user.name name')
            self.add_command('git config --global user.email email')

    @_called_execute
    def git_add(self):
        self.add_command('git add .')

    @_called_execute
    def git_commit(self, message: str):
        self.add_command(f"git commit -m '{message}'")

    @_called_execute
    def show_git_log(self):
        self.add_command('git log')

    @_called_execute
    def save_file_content(self, file_path: str):
        self.commands.append(f'echo start cat for {file_path}')
        self.commands.append(f'cat /root/{file_path}')
        self.commands.append(f'echo end cat for {file_path}')

    @_called_execute
    def add_file(self, file_path: str, text: str = None):
        command = f'touch {file_path}'
        if text:
            command = f'echo "{text}" >> {file_path}'
        self.add_command(command)

    @_not_called_execute
    def get_file_text(self, file_path: str) -> List[str]:
        file = self.file_system.get_file_from_root(file_path)
        return file.lines

    @_print_logs_when_test_fails
    @_not_called_execute
    def assert_directory_exists(self, path: str):
        self._file_or_directory_exists_in_file_system(path)

    @_print_logs_when_test_fails
    @_not_called_execute
    def assert_text_in_logs(self, position_in_logs: int, expected_text: str):
        self.assertTrue(position_in_logs < len(self.logs))
        self.assertEqual(expected_text, self.logs[position_in_logs])

    @_print_logs_when_test_fails
    @_not_called_execute
    def assert_text_not_in_logs(self, position_in_logs: int, unexpected_text: str):
        self.assertNotEqual(unexpected_text, self.logs[position_in_logs])

    @_print_logs_when_test_fails
    @_not_called_execute
    def assert_file_exists(self, expected_path):
        self._file_or_directory_exists_in_file_system(expected_path)

    def _generate_commands_string_to_pass_to_run(self) -> str:
        return f'/bin/sh -c "{"; ".join(self.commands)}"'

    def _file_or_directory_exists_in_file_system(self, path: str):
        self.assertTrue(self.file_system.get_file_from_root(path) is not None)
