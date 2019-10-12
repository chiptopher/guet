import datetime
import os
import subprocess
from os.path import join, expanduser, isdir
from shutil import rmtree

from e2e.e2etest import E2ETest
from guet.gateways.gateway import PairSetGateway


class TestGuetCommitRotatesAuthor(E2ETest):

    def commits_swaps_pairs_once(self):

        test_directory = join(expanduser('~'), 'test')
        if isdir(test_directory):
            rmtree(test_directory)

        self.guet_init()

        self.guet_add('initials', 'name', 'email@localhost')
        self.guet_add('initials2', 'name2', 'email2@localhost')

        os.mkdir(test_directory)
        open(join(expanduser('~'), 'test', 'file1'), 'w').close()

        self.git_init('.', test_directory)
        twenty_four_hours = 86400000
        twenty_four_hours_ago = round((datetime.datetime.utcnow().timestamp() - 1) * 1000) - twenty_four_hours
        pair_set_gateway = PairSetGateway()
        pair_set_gateway.add_pair_set(twenty_four_hours_ago)

        self.guet_start(directory_to_execute_in=join(expanduser('~'), 'test'))
        self.git_add('.', test_directory)

        process = subprocess.Popen(['git', 'commit', '-m', '\"Initial commit\"'], cwd=test_directory, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        res = process.communicate()
        expected_output = "\nYou have not reset pairs in over twenty four hours!\nPlease reset your pairs by using guet set and including your pairs' initials\n\n"
        self.assertEqual(expected_output, res[1].decode('utf-8'))
        rmtree(test_directory)
