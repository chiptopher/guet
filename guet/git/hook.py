from guet.files.read_lines import read_lines
from guet.git.errors import NotGuetHookError

GUET_HOOK_FILE = [
    '#! /usr/bin/env python3',
    'from guet.hooks import manage',
    'import sys',
    'manage(sys.argv[0])',
]


class Hook:
    def __init__(self, path_to_hook: str):
        self.path = path_to_hook
        _content = read_lines(path_to_hook)
        if _content != GUET_HOOK_FILE:
            raise NotGuetHookError()
        self.content = _content
