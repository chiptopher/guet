from os.path import join

from guet import constants
from guet.config import CONFIGURATION_DIRECTORY
from guet.config.committer import Committer


def set_committer_as_author(committer: Committer):
    author_name_file = open(join(CONFIGURATION_DIRECTORY, constants.AUTHOR_NAME), 'w')
    author_name_file.write(f'{committer.name}\n')
    author_name_file.close()
    author_email_file = open(join(CONFIGURATION_DIRECTORY, constants.AUTHOR_EMAIL), 'w')
    author_email_file.write(f'{committer.email}\n')
    author_email_file.close()
