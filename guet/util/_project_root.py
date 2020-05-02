from os import getcwd
from pathlib import Path

from guet.util import recursive_directory_find


def project_root() -> Path:
    return recursive_directory_find(Path(getcwd()), '.git')
