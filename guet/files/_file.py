from pathlib import Path
from typing import List, Callable

from guet.files.read_lines import read_lines

from guet.files.write_lines import write_lines


class File:
    def __init__(self, absolute_path: Path):
        self._content = None
        self._absolute_path = absolute_path

    def read(self) -> List[str]:
        try:
            self._content = read_lines(self._absolute_path)
        except FileNotFoundError:
            self._content = []
        return self._content

    def write(self, new_content: List[str]):
        self._content = new_content

    def save(self):
        if self._content is not None:
            write_lines(self._absolute_path, self._content)

    def overwrite(self, matcher: Callable[[str], bool], new_line: str):
        for index, line in enumerate(self.read()):
            if matcher(line):
                self._content[index] = new_line
