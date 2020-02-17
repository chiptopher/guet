from os import chmod, stat

from guet.files.read_lines import read_lines
from guet.files.write_lines import write_lines
from guet.git.errors import NotGuetHookError

GUET_HOOK_FILE = [
    '#! /usr/bin/env python3',
    'from guet.hooks import manage',
    'import sys',
    'manage(sys.argv[0])',
]


class Hook:
    def __init__(self, path_to_hook: str, *, create: bool = False):
        self.path = path_to_hook
        self.content = self._parse_file_content(create, path_to_hook)

    @staticmethod
    def _parse_file_content(create, path_to_hook):
        try:
            _content = read_lines(path_to_hook)
        except FileNotFoundError:
            if create:
                _content = GUET_HOOK_FILE
            else:
                raise
        if _content != GUET_HOOK_FILE:
            raise NotGuetHookError()
        return _content

    def save(self):
        write_lines(self.path, self.content)
        status = stat(self.path)
        chmod(self.path, status.st_mode | 0o111)
