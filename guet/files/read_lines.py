from pathlib import Path
from typing import List


def read_lines(path: Path) -> List[str]:
    return _read_lines_from_path(path)


def _read_lines_from_path(path: Path) -> List[str]:
    all_lines = path.read_text().split('\n')
    if all_lines[len(all_lines) - 1] == '':
        del all_lines[len(all_lines) - 1]
    return all_lines
