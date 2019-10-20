from os.path import join, expanduser
from typing import List

from guet import constants
from guet.config import configuration_directory
from guet.config.committer import Committer


def set_committers(committers: List[Committer]):
    f = open(join(configuration_directory, constants.COMMITTER_NAMES), 'w')
    for committer in committers:
        f.write(f'{committer.name} <{committer.email}>\n')
