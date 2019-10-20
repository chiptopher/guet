from os.path import isdir

from guet.config import configuration_directory


def already_initialized():
    return isdir(configuration_directory)
