from os.path import expanduser
from pathlib import Path


def recursive_directory_find(starting_path: Path, directory_name: str) -> Path:
    if str(starting_path) == expanduser('~'):
        raise FileNotFoundError()
    joined = starting_path.joinpath(directory_name)
    if joined.is_dir():
        return starting_path
    else:
        return recursive_directory_find(starting_path.parent, directory_name)
