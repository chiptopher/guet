from os import getcwd

from guet.util import recursive_directory_find


def project_root() -> str:
    return recursive_directory_find(getcwd(), '.git')
