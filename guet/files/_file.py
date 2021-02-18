from os import remove
from pathlib import Path
from typing import Callable, List

from guet.files.read_lines import read_lines
from guet.files.write_lines import write_lines


class File:
    def __init__(self, absolute_path: Path):
        self._content = None
        self._absolute_path = absolute_path
        self._marked_for_deletion = False
        self._written_to = False

    def read(self) -> List[str]:
        try:
            self._content = read_lines(self._absolute_path)
        except FileNotFoundError:
            self._content = []
        return self._content

    def write(self, new_content: List[str]):
        self._written_to = True
        self._content = new_content
        self._marked_for_deletion = False

    def save(self):
        if self._marked_for_deletion:
            remove(self._absolute_path)
        elif self._content is not None and self._written_to:
            write_lines(self._absolute_path, self._content)

    def overwrite(self, matcher: Callable[[str], bool], new_line: str):
        for index, line in enumerate(self.read()):
            if matcher(line):
                self._content[index] = new_line

    def delete(self):
        self._marked_for_deletion = True
