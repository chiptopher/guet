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

        process = subprocess.Popen(['guet', 'init'])
        process.wait()

        pair1 = dict(
            initials='initials',
            name='name',
            email='email@localhost'
        )
        pair2 = dict(
            initials='initials2',
            name='name2',
            email='email2@localhost'
        )

        process = subprocess.Popen(['guet', 'add', pair1['initials'], pair1['name'], pair1['email']])
        process.wait()
        process = subprocess.Popen(['guet', 'add', pair2['initials'], pair2['name'], pair2['email']])
        process.wait()
        os.mkdir(join(expanduser('~'), 'test'))
        open(join(expanduser('~'), 'test', 'file1'), 'w').close()
        process = subprocess.Popen(['git', 'init'], cwd=join(expanduser('~'), 'test'))
        process.wait()
        process = subprocess.Popen(['guet', 'set', pair1['initials'], pair2['initials']], cwd=join(expanduser('~'), 'test'))
        process.wait()
        process = subprocess.Popen(['guet', 'start', '--python3'], cwd=join(expanduser('~'), 'test'))
        process.wait()
        process = subprocess.Popen(['git', 'add', '.'], cwd=join(expanduser('~'), 'test'))
        process.wait()
        process = subprocess.Popen(['git', 'commit', '-m', '\"Initial commit\"'], cwd=join(expanduser('~'), 'test'))
        process.wait()

        guet_path = join(expanduser('~'), const.APP_FOLDER_NAME)

        with open(join(guet_path, const.AUTHOR_NAME)) as author_file:
            author_name = author_file.readline()
        self.assertEqual(pair2['name'], author_name)

        with open(join(guet_path, const.AUTHOR_EMAIL)) as author_file:
            author_email = author_file.readline()
        self.assertEqual(pair2['email'], author_email)

        rmtree(join(expanduser('~'), 'test'))

    def test_mob_participants_can_swap_multiple_times(self):

        if isdir(join(expanduser('~'), 'test')):
            rmtree(join(expanduser('~'), 'test'))

        process = subprocess.Popen(['guet', 'init'])
        process.wait()

        pair1 = dict(
            initials='initials',
            name='name',
            email='email@localhost'
        )
        pair2 = dict(
            initials='initials2',
            name='name2',
            email='email2@localhost'
        )

        pair3 = dict(
            initials='initials3',
            name='name3',
            email='email3@localhost'
        )

        process = subprocess.Popen(['guet', 'add', pair1['initials'], pair1['name'], pair1['email']])
        process.wait()
        process = subprocess.Popen(['guet', 'add', pair2['initials'], pair2['name'], pair2['email']])
        process.wait()
        process = subprocess.Popen(['guet', 'add', pair3['initials'], pair3['name'], pair3['email']])
        process.wait()
        os.mkdir(join(expanduser('~'), 'test'))
        open(join(expanduser('~'), 'test', 'file1'), 'w').close()
        process = subprocess.Popen(['git', 'init'], cwd=join(expanduser('~'), 'test'))
        process.wait()
        process = subprocess.Popen(['guet', 'set', pair1['initials'], pair2['initials'], pair3['initials']], cwd=join(expanduser('~'), 'test'))
        process.wait()
        process = subprocess.Popen(['guet', 'start', '--python3'],
                                   cwd=join(expanduser('~'), 'test'))
        process.wait()
        process = subprocess.Popen(['git', 'add', '.'], cwd=join(expanduser('~'), 'test'))
        process.wait()
        process = subprocess.Popen(['git', 'commit', '-m', '\"Initial commit\"'], cwd=join(expanduser('~'), 'test'))
        process.wait()
        open(join(expanduser('~'), 'test', 'file2'), 'w').close()
        process = subprocess.Popen(['git', 'add', '.'], cwd=join(expanduser('~'), 'test'))
        process.wait()
        process = subprocess.Popen(['git', 'commit', '-m', '\"Commit 2\"'], cwd=join(expanduser('~'), 'test'))
        process.wait()

        guet_path = join(expanduser('~'), const.APP_FOLDER_NAME)

        with open(join(guet_path, const.AUTHOR_NAME)) as author_file:
            author_name = author_file.readline()
        self.assertEqual(pair3['name'], author_name)

        with open(join(guet_path, const.AUTHOR_EMAIL)) as author_file:
            author_email = author_file.readline()
        self.assertEqual(pair3['email'], author_email)

        rmtree(join(expanduser('~'), 'test'))

    def test_second_commit_uses_second_pair_name_and_email(self):

        if isdir(join(expanduser('~'), 'test')):
            rmtree(join(expanduser('~'), 'test'))

        process = subprocess.Popen(['guet', 'init'])
        process.wait()

        pair1 = dict(
            initials='initials',
            name='name',
            email='email@localhost'
        )
        pair2 = dict(
            initials='initials2',
            name='name2',
            email='email2@localhost'
        )

        os.mkdir(join(expanduser('~'), 'test'))
        process = subprocess.Popen(['guet', 'add', pair1['initials'], pair1['name'], pair1['email']])
        process.wait()
        process = subprocess.Popen(['guet', 'add', pair2['initials'], pair2['name'], pair2['email']])
        process.wait()
        open(join(expanduser('~'), 'test', 'file1'), 'w').close()
        process = subprocess.Popen(['git', 'init'], cwd=join(expanduser('~'), 'test'))
        process.wait()
        process = subprocess.Popen(['guet', 'set', pair1['initials'], pair2['initials']], cwd=join(expanduser('~'), 'test'))
        process.wait()
        process = subprocess.Popen(['guet', 'start', '--python3'],
                                   cwd=join(expanduser('~'), 'test'))
        process.wait()
        process = subprocess.Popen(['git', 'add', '.'], cwd=join(expanduser('~'), 'test'))
        process.wait()
        process = subprocess.Popen(['git', 'commit', '-m', '\"1\"'], cwd=join(expanduser('~'), 'test'))
        process.wait()
        open(join(expanduser('~'), 'test', 'file2'), 'w').close()
        process = subprocess.Popen(['git', 'add', '.'], cwd=join(expanduser('~'), 'test'))
        process.wait()
        process = subprocess.Popen(['git', 'commit', '-m', '\"2\"'], cwd=join(expanduser('~'), 'test'))
        process.wait()
        process = subprocess.Popen(['git', 'log'], stdout=subprocess.PIPE, cwd=join(expanduser('~'), 'test'))
        output = process.communicate()[0].decode('utf-8')
        fist_commit = output.split('commit')[1]
        self.assertTrue('Author: {} <{}>'.format(pair2['name'], pair2['email']) in fist_commit)

        rmtree(join(expanduser('~'), 'test'))