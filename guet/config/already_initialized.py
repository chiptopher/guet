from os.path import isdir

from guet.config import CONFIGURATION_DIRECTORY


def already_initialized():
    return isdir(CONFIGURATION_DIRECTORY)
