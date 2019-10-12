from os import getcwd
from os.path import join


def git_path_from_cwd():
    return join(getcwd(), '.git')


def git_hook_path_from_cwd():
    return join(git_path_from_cwd(), 'hooks')
