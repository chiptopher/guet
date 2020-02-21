from os import getcwd
from os.path import join


def git_path_from_cwd():
    return join(getcwd(), '.git')
