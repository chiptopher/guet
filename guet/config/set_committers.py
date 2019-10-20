from os.path import join, expanduser
from typing import List

from guet import constants
from guet.config import configuration_directory


class CommitterInput:
    def __init__(self, name: str, email: str):
        self.name = name
        self.email = email


def set_committers(committers: List[CommitterInput]):
    f = open(join(configuration_directory, constants.COMMITTER_NAMES), 'w')
    for committer in committers:
        f.write(f'{committer.name} <{committer.email}>\n')
