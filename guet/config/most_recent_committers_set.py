from os.path import join

from guet import constants
from guet.config import configuration_directory


def most_recent_committers_set():
    f = open(join(configuration_directory, constants.COMMITTERS_SET), 'r')
    line = f.readline()
    f.close()
    split = line.rstrip().split(',')
    return int(split[len(split)-1])

