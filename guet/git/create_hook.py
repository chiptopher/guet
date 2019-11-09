from enum import Enum
from os import chmod, stat
from os.path import join
from guet.git._hook_mode import HookMode

HOOK_FILE_LINES = [
    '#! /usr/bin/env python3\n',
    'from guet.hooks import manage\n',
    'import sys\n',
    'manage(sys.argv[0])\n',
]


class Hooks(Enum):
    PRE_COMMIT = 'pre-commit'
    COMMIT_MSG = 'commit-msg'
    POST_COMMIT = 'post-commit'


def create_hook(hook_folder_path: str, hook: Hooks, create_mode: HookMode):
    final_hook_path = join(hook_folder_path, create_mode(hook.value))
    f = open(final_hook_path, 'w')
    f.writelines(HOOK_FILE_LINES)
    f.close()

    st = stat(final_hook_path)
    chmod(final_hook_path, st.st_mode | 0o111)
