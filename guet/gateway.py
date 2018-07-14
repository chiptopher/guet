"""
Copyright 2018 Christopher M. Boyer

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

    http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.
"""

import sys
from os.path import expanduser, abspath, join, pardir, isdir, isfile
import os
from os import mkdir, getcwd
import sqlite3
from collections import namedtuple
from . import constants
from .stdout_manager import StdoutManager

committer_result = namedtuple('CommitterOutput', 'initials name email')


class CommitterInput:
    def __init__(self, name: str, email: str):
        self.name = name
        self.email = email

    def __eq__(self, other):
        return self.email is other.email and self.name is other.name


class PrintGateway:
    def __init__(self, stdout_manager=StdoutManager.get_instance()):
        self._stdout_manager = stdout_manager

    def print(self, text):
        original_stdout = sys.stdout
        sys.stdout = self._stdout_manager.get_stdout()
        print(text)
        sys.stdout = original_stdout


class GitGateway:
    def __init__(self, parent_dir: str = getcwd()):
        self._parent_dir = parent_dir

    def add_commit_msg_hook(self):
        lines = [
            "#!/bin/sh", "FILE_LOCATION=~/.guet/committernames", 'CO_AUTHOR="Co-authored-by:"',
            'echo "\\n\\n" >> "$1"', 'while read committer; do',
            '	echo "$CO_AUTHOR $committer" >> "$1"', 'done <$FILE_LOCATION'
        ]
        hook_path = join(self._parent_dir, '.git', 'hooks', 'commit-msg')
        f = open(hook_path, "w+")
        st = os.stat(hook_path)
        os.chmod(hook_path, st.st_mode | 0o111)
        for line in lines:
            f.write(line + '\n')
        f.close()

    def commit_msg_hook_exists(self):
        return isfile(join(self._parent_dir, '.git', 'hooks', 'commit-msg'))

    def git_present(self):
        return isdir(join(os.getcwd(), '.git'))


class UserGateway:
    def __init__(self, connection_path: str = expanduser('~')):
        self._connection_path = self._append_data_source_to(connection_path)
        self._connection = None

    @classmethod
    def _append_data_source_to(cls, path):
        return join(path, join(constants.APP_FOLDER_NAME, constants.DATA_SOURCE_NAME))

    def add_user(self, initials: str, name: str, email: str):
        if self.get_user(initials):
            self.delete_user(initials)
        self._connection = sqlite3.connect(self._connection_path)
        query = "INSERT INTO committer(`initials`, `name`, `email`) VALUES (?, ?, ?)"
        self._connection.cursor().execute(query, (
            initials,
            name,
            email,
        ))
        self._connection.commit()
        self._connection.close()

    def get_user(self, initials: str):
        self._connection = sqlite3.connect(self._connection_path)
        cursor = self._connection.cursor()
        cursor.execute("SELECT * FROM committer WHERE initials=?", (initials, ))
        result = cursor.fetchone()
        self._connection.close()
        if result:
            return committer_result(initials=result[0], name=result[1], email=result[2])

    def delete_user(self, initials):
        self._connection = sqlite3.connect(self._connection_path)
        cursor = self._connection.cursor()
        cursor.execute("DELETE FROM committer WHERE initials=?", (initials, ))
        self._connection.commit()
        self._connection.close()


class FileGateway:
    def __init__(self, path: str = expanduser("~")):
        self._path = path

    def initialize(self):
        app_folder_path = self._create_app_path()
        mkdir(app_folder_path)
        connection = sqlite3.connect(join(app_folder_path, constants.DATA_SOURCE_NAME))
        connection.execute("""CREATE TABLE committer
                              (initials TEXT NOT NULL PRIMARY KEY,
                               name TEXT NOT NULL,
                               email TEXT NOT NULL)""")
        connection.close()
        committer_names = join(app_folder_path, constants.COMMITTER_NAMES)
        f = open(committer_names, "w+")
        f.close()

    def set_committers(self, committers: list):
        with open(join(self._path, constants.APP_FOLDER_NAME, constants.COMMITTER_NAMES),
                  'w') as committers_file:
            committers_file.seek(0)
            committers_file.truncate()
            for committer in committers:
                committers_file.write('{} <{}>\n'.format(committer.name, committer.email))

    def _create_app_path(self):
        return join(abspath(self._path), constants.APP_FOLDER_NAME)

    def path_exists(self):
        return isdir(self._create_app_path())

    @staticmethod
    def home_dir(file_dir):
        return abspath(join(file_dir, pardir))
