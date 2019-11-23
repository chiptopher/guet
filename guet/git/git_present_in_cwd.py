from os.path import isdir, join
from os import getcwd


def git_present_in_cwd():
    return isdir(join(getcwd(), '.git'))
