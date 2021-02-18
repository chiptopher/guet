from typing import List

from guet.files import File, FileSystem
from guet.util import project_root

from .hook import shared_hook_lines

_FILE_NAMES = [
    'pre-commit',
    'post-commit',
    'commit-msg',
    'pre-commit-guet',
    'post-commit-guet',
    'commit-msg-guet',
]

def _is_guet_file(content: List[str]) -> bool:
    return content[1:] == shared_hook_lines()


def all_guet_hooks(file_system: FileSystem) -> List[File]:
    git_hooks_path = project_root().joinpath('.git').joinpath('hooks')
    found = []
    for file_name in _FILE_NAMES:
        file = file_system.get(git_hooks_path.joinpath(file_name))
        if _is_guet_file(file.read()):
            found.append(file)

    return found
