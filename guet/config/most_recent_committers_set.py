from os.path import join

from guet import constants
from guet.config import CONFIGURATION_DIRECTORY


def most_recent_committers_set():
    set_committers_file = open(join(CONFIGURATION_DIRECTORY, constants.COMMITTERS_SET), 'r')
    line = set_committers_file.readline()
    set_committers_file.close()
    split = line.rstrip().split(',')
    return int(split[len(split)-1])
