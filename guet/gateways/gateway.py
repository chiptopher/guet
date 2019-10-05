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

import datetime
import os
import sqlite3
import subprocess
from collections import namedtuple
from os import mkdir, getcwd
from os.path import expanduser, abspath, join, pardir, isdir, isfile

from guet import constants
from guet.gateways.errors import UninitializedError

committer_result = namedtuple('CommitterOutput', 'initials name email')
pair_set_result = namedtuple('PairSet', 'id set_time')
pair_set_committer_result = namedtuple('PairSetCommitter', 'id committer_initials pair_set_id')


class CommitterInput:
    def __init__(self, name: str, email: str):
        self.name = name
        self.email = email

    def __eq__(self, other):
        return self.email is other.email and self.name is other.name


class _SQLGateway:
    def __init__(self, connection_path: str = expanduser('~')):
        self._connection_path = self._append_data_source_to(connection_path)
        self._connection = None

    @classmethod
    def _append_data_source_to(cls, path):
        return join(path, join(constants.APP_FOLDER_NAME, constants.DATA_SOURCE_NAME))

    def has_been_initialized(self):
        return isfile(self._connection_path)


class PairSetGatewayCommitterGateway(_SQLGateway):
    def add_pair_set_committer(self, committer_initials, pair_set_id):
        self._connection = sqlite3.connect(self._connection_path)
        query = "INSERT INTO pair_set_committer(`committer_initials`, `pair_set_id`) VALUES (?, ?)"
        self._connection.cursor().execute(query, (
            committer_initials,
            pair_set_id,
        ))
        self._connection.commit()
        self._connection.close()

    def get_pair_set_committers_by_pair_set_id(self, pair_set_id: int):
        self._connection = sqlite3.connect(self._connection_path)
        query = "SELECT * FROM pair_set_committer WHERE pair_set_id=?"
        result = self._connection.cursor().execute(query, (pair_set_id,)).fetchall()
        self._connection.commit()
        self._connection.close()
        return list(
            map(lambda i: pair_set_committer_result(id=i[0], pair_set_id=i[2], committer_initials=i[1]), result))


class PairSetGateway(_SQLGateway):
    def add_pair_set(self, set_timestamp: int = round(datetime.datetime.utcnow().timestamp() * 1000)):
        self._connection = sqlite3.connect(self._connection_path)
        query = "INSERT INTO pair_set(`set_time`) VALUES (?)"
        cursor = self._connection.cursor()
        cursor.execute(query, (
            set_timestamp,
        ))
        row_id = cursor.lastrowid
        self._connection.commit()
        self._connection.close()
        return row_id

    def get_pair_set(self, id: int):
        self._connection = sqlite3.connect(self._connection_path)
        query = "SELECT * FROM pair_set WHERE id=?"
        result = self._connection.cursor().execute(query, (id,)).fetchone()
        self._connection.commit()
        self._connection.close()
        return pair_set_result(id=id, set_time=result[1])

    def get_most_recent_pair_set(self):
        self._connection = sqlite3.connect(self._connection_path)
        query = "SELECT * FROM pair_set ORDER BY set_time DESC"
        result = self._connection.execute(query).fetchone()
        return pair_set_result(id=result[0], set_time=result[1])


class UserGateway(_SQLGateway):

    def add_user(self, initials: str, name: str, email: str):
        if self.has_been_initialized():
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
        else:
            raise UninitializedError()

    def get_user(self, initials: str):
        self._connection = sqlite3.connect(self._connection_path)
        cursor = self._connection.cursor()
        cursor.execute("SELECT * FROM committer WHERE initials=?", (initials,))
        result = cursor.fetchone()
        self._connection.close()
        if result:
            return committer_result(initials=result[0], name=result[1], email=result[2])

    def delete_user(self, initials):
        self._connection = sqlite3.connect(self._connection_path)
        cursor = self._connection.cursor()
        cursor.execute("DELETE FROM committer WHERE initials=?", (initials,))
        self._connection.commit()
        self._connection.close()


class FileGateway:
    def __init__(self, path: str = expanduser("~"), subprocess_module=subprocess):
        self._path = path
        self._subprocess = subprocess_module

    def initialize(self):
        app_folder_path = self._create_app_path()
        mkdir(app_folder_path)
        connection = sqlite3.connect(join(app_folder_path, constants.DATA_SOURCE_NAME))
        connection.execute("""CREATE TABLE committer
                              (initials TEXT NOT NULL PRIMARY KEY,
                               name TEXT NOT NULL,
                               email TEXT NOT NULL)""")
        connection.execute("""CREATE TABLE pair_set
                              (id INTEGER NOT NULL PRIMARY KEY,
                              set_time INTEGER NOT NULL)
                              """)
        connection.execute("""CREATE TABLE pair_set_committer
                              (id INTEGER NOT NULL PRIMARY KEY,
                              committer_initials TEXT NOT NULL,
                              pair_set_id INTEGER NOT NULL,
                              FOREIGN KEY (pair_set_id) REFERENCES pair_set(id),
                              FOREIGN KEY (committer_initials) REFERENCES comitter(initials)
                              )
                              """)
        connection.close()

        def create_fule_with_name(file_name: str):
            f = open(file_name, 'w+')
            f.close()

        create_fule_with_name(join(app_folder_path, constants.COMMITTER_NAMES))
        create_fule_with_name(join(app_folder_path, constants.AUTHOR_EMAIL))
        create_fule_with_name(join(app_folder_path, constants.AUTHOR_NAME))

    def set_committers(self, committers: list):
        with open(join(self._path, constants.APP_FOLDER_NAME, constants.COMMITTER_NAMES),
                  'w') as committers_file:
            committers_file.seek(0)
            committers_file.truncate()
            for committer in committers:
                committers_file.write('{} <{}>\n'.format(committer.name, committer.email))

    def get_committers(self):
        committers = []
        with open(join(self._path, constants.APP_FOLDER_NAME, constants.COMMITTER_NAMES), 'r') as commiters_file:
            for committer in commiters_file.readlines():
                split = committer.split(' ')
                name = ' '.join(split[:len(split) - 1])
                committers.append(
                    committer_result(name=name, email=split[len(split) - 1].strip().strip('<').strip('>'), initials=''))
        return committers

    def _create_app_path(self):
        return join(abspath(self._path), constants.APP_FOLDER_NAME)

    def path_exists(self):
        return isdir(self._create_app_path())

    @staticmethod
    def home_dir(file_dir):
        return abspath(join(file_dir, pardir))

    def set_author_name(self, name: str):
        with open(join(self._path, constants.APP_FOLDER_NAME, constants.AUTHOR_NAME), 'w') as author_name_file:
            author_name_file.seek(0)
            author_name_file.truncate()
            author_name_file.write(name)
            process = self._subprocess.Popen(['git', 'config', 'user.name', name])
            process.wait()

    def set_author_email(self, email: str):
        with open(join(self._path, constants.APP_FOLDER_NAME, constants.AUTHOR_EMAIL), 'w') as author_email_file:
            author_email_file.seek(0)
            author_email_file.truncate()
            author_email_file.write(email)
            process = self._subprocess.Popen(['git', 'config', 'user.email', email])
            process.wait()
