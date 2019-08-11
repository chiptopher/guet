import os
import subprocess
from os.path import join, expanduser, isdir
from shutil import rmtree

from e2e.e2etest import E2ETest
from guet import constants as const


class TestGuetCommitRotatesAuthor(E2ETest):

    def test_commits_swaps_pairs_once(self):

        if isdir(join(expanduser('~'), 'test')):
            rmtree(join(expanduser('~'), 'test'))

        self.guet_init()
        self.guet_add('initials', 'name', 'email@localhost')
        self.guet_add('initials2', 'name2', 'email2@localhost')

        os.mkdir(join(expanduser('~'), 'test'))
        open(join(expanduser('~'), 'test', 'file1'), 'w').close()

        self.git_init('.', join(expanduser('~'), 'test'))
        self.guet_start(directory_to_execute_in=join(expanduser('~'), 'test'))
        self.guet_set(['initials', 'initials2'])
        self.git_add('.', join(expanduser('~'), 'test'))
        self.git_commit('\"Initial commit\"', join(expanduser('~'), 'test'))

        guet_path = join(expanduser('~'), const.APP_FOLDER_NAME)

        with open(join(guet_path, const.AUTHOR_NAME)) as author_file:
            author_name = author_file.readline()
        self.assertEqual('name2', author_name)

        with open(join(guet_path, const.AUTHOR_EMAIL)) as author_file:
            author_email = author_file.readline()
        self.assertEqual('email2@localhost', author_email)

        rmtree(join(expanduser('~'), 'test'))

    def test_mob_participants_can_swap_multiple_times(self):

        test_directory = join(expanduser('~'), 'test')
        if isdir(test_directory):
            rmtree(test_directory)

        self.guet_init()
        self.guet_add('initials', 'name', 'email@localhost')
        self.guet_add('initials2', 'name2', 'email2@localhost')
        self.guet_add('initials3', 'name3', 'email3@localhost')

        os.mkdir(test_directory)
        open(join(expanduser('~'), 'test', 'file1'), 'w').close()

        self.git_init('.', test_directory)
        self.guet_set(['initials', 'initials2', 'initials3'], join(expanduser('~'), 'test'))
        self.guet_start(directory_to_execute_in=join(expanduser('~'), 'test'))
        self.git_add('.', test_directory)
        self.git_commit('\"Initial commit\"', test_directory)

        open(join(expanduser('~'), 'test', 'file2'), 'w').close()

        self.git_add('.', test_directory)
        self.git_commit('\"Commit 2\"', test_directory)

        guet_path = join(expanduser('~'), const.APP_FOLDER_NAME)

        with open(join(guet_path, const.AUTHOR_NAME)) as author_file:
            author_name = author_file.readline()
        self.assertEqual('name3', author_name)

        with open(join(guet_path, const.AUTHOR_EMAIL)) as author_file:
            author_email = author_file.readline()
        self.assertEqual('email3@localhost', author_email)

        rmtree(test_directory)

    def test_second_commit_uses_second_pair_name_and_email(self):

        test_directory = join(expanduser('~'), 'test')
        if isdir(test_directory):
            rmtree(test_directory)

        self.guet_init()

        os.mkdir(test_directory)

        self.guet_add('initials', 'name', 'email@localhost')
        self.guet_add('initials2', 'name2', 'email2@localhost')

        open(join(expanduser('~'), 'test', 'file1'), 'w').close()
        self.git_init('.', test_directory)

        self.guet_set(['initials', 'initials2'])
        self.guet_start(directory_to_execute_in=join(expanduser('~'), 'test'))
        self.git_add('.', test_directory)
        self.git_commit('\"1\"', test_directory)

        open(join(expanduser('~'), 'test', 'file2'), 'w').close()

        self.git_add('.', test_directory)
        self.git_commit('\"2\"', test_directory)

        output = self.git_log(test_directory)
        fist_commit = output.split('commit')[1]
        self.assertTrue('Author: {} <{}>'.format('name2', 'email2@localhost') in fist_commit)

        rmtree(test_directory)