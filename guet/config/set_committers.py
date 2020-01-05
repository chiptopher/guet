from os.path import join
from typing import List

from guet import constants
from guet.config import CONFIGURATION_DIRECTORY
from guet.config.add_committer import add_committer
from guet.config.committer import Committer
from guet.files.write_lines import write_lines


def set_committers(committers: List[Committer]):
    write_lines(join(CONFIGURATION_DIRECTORY, constants.COMMITTERS), [])
    for committer in committers:
        add_committer(committer.initials, committer.name, committer.email)
