from os import chmod, stat

from guet.files.read_lines import read_lines
from guet.files.write_lines import write_lines

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

    def __repr__(self) -> str:
        return f'Hook: path: {self.path}, content: {self.content}'

    def is_guet_hook(self):
        return self.content == GUET_HOOK_FILE

    @staticmethod
    def _parse_file_content(create, path_to_hook):
        _content = Hook._get_file_content(path_to_hook, create)
        if _content != GUET_HOOK_FILE:
            _content = Hook._handle_mismatched_content(_content, create)
        return _content

    @staticmethod
    def _handle_mismatched_content(_content, create):
        if create:
            _content = GUET_HOOK_FILE
        return _content

    @staticmethod
    def _get_file_content(path_to_hook, create):
        try:
            _content = read_lines(path_to_hook)
        except FileNotFoundError:
            if create:
                _content = GUET_HOOK_FILE
            else:
                raise
        return _content

    def save(self):
        write_lines(self.path, self.content)
        status = stat(self.path)
        chmod(self.path, status.st_mode | 0o111)
