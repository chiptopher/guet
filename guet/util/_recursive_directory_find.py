from pathlib import Path
from os.path import expanduser


def recursive_directory_find(starting_path: str, directory_name: str) -> str:
    return _recursive_directory_find(Path(starting_path), directory_name)


def _recursive_directory_find(path: Path, directory_name: str) -> str:
    if str(path) == expanduser('~'):
        raise FileNotFoundError()
    joined_with_driectory = path.joinpath(directory_name)
    if joined_with_driectory.is_dir():
        return str(path)
    else:
        return _recursive_directory_find(path.parent, directory_name)
