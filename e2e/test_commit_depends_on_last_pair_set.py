import datetime
import os
import subprocess
from os.path import join, expanduser, isdir
from shutil import rmtree

from e2e.e2etest import E2ETest
from guet.gateways.gateway import PairSetGateway


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
        twenty_four_hours = 86400000
        twenty_four_hours_ago = round((datetime.datetime.utcnow().timestamp() - 1) * 1000) - twenty_four_hours
        pair_set_gateway = PairSetGateway()
        pair_set_gateway.add_pair_set(twenty_four_hours_ago)
        process = subprocess.Popen(['guet', 'start', pair1['initials'], pair2['initials']], cwd=join(expanduser('~'), 'test'))
        process.wait()
        process = subprocess.Popen(['git', 'add', '.'], cwd=join(expanduser('~'), 'test'))
        process.wait()
        process = subprocess.Popen(['git', 'commit', '-m', '\"Initial commit\"'], cwd=join(expanduser('~'), 'test'), stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        res = process.communicate()
        expected_output = 'Must set pairs again\n'
        self.assertEqual(expected_output, res[1].decode('utf-8'))
        rmtree(join(expanduser('~'), 'test'))