from os import chmod, stat
from pathlib import Path
from shutil import which
from typing import List

from guet.files.read_lines import read_lines
from guet.files.write_lines import write_lines


def shared_hook_lines() -> List[str]:
    return [
        'from guet.hooks import run',
        'import sys',
        'run(sys.argv[0])',
    ]


PYTHON_GUET_HOOK = ['#! /usr/bin/env python'] + shared_hook_lines()

PYTHON3_GUET_HOOK = ['#! /usr/bin/env python3'] + shared_hook_lines()


class Hook:

    def __init__(self, path_to_hook: Path, *, create: bool = False):
        self.path = path_to_hook
        self.content = self._parse_file_content(create, path_to_hook)

    def __repr__(self) -> str:
        return f'Hook: path: {self.path}, content: {self.content}'

    def is_guet_hook(self):
        return self.content == PYTHON3_GUET_HOOK or self.content == PYTHON_GUET_HOOK

    @staticmethod
    def _parse_file_content(create, path_to_hook):
        _content = Hook._get_file_content(path_to_hook, create)
        if _content not in (PYTHON3_GUET_HOOK, PYTHON_GUET_HOOK):
            _content = Hook._handle_mismatched_content(_content, create)
        return _content

    @staticmethod
    def _handle_mismatched_content(_content, create):
        if create:
            _content = PYTHON3_GUET_HOOK
        return _content

    @staticmethod
    def _get_file_content(path_to_hook, create: bool):
        try:
            _content = read_lines(path_to_hook)
        except FileNotFoundError:
            if create:
                if not which('python3'):
                    _content = PYTHON_GUET_HOOK
                else:
                    _content = PYTHON3_GUET_HOOK
            else:
                raise
        return _content

    def save(self):
        write_lines(self.path, self.content)
        status = stat(str(self.path))
        chmod(str(self.path), status.st_mode | 0o111)
