from pathlib import Path
from typing import List


def _append_newline_if_not_present(line: str):
    if line.endswith('\n'):
        return line
    else:
        return f'{line}\n'


def _format_lines(lines: List[str]) -> str:
    return ''.join([_append_newline_if_not_present(line) for line in lines])


def _write_lines_to_path(path: Path, lines: List[str]) -> None:
    text = _format_lines(lines)
    path.write_text(text)


def write_lines(path: Path, lines: List[str]) -> None:
    return _write_lines_to_path(path, lines)
