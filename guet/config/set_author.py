from os.path import join

from guet import constants
from guet.config import configuration_directory
from guet.config.committer import Committer


def set_committer_as_author(committer: Committer):
    f = open(join(configuration_directory, constants.AUTHOR_NAME), 'w')
    f.write(committer.name)
    f.close()
    f = open(join(configuration_directory, constants.AUTHOR_EMAIL), 'w')
    f.write(committer.email)
    f.close()
